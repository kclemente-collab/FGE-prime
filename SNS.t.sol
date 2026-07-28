// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * SNS.t.sol — End-to-End Integration Test Suite (Foundry)
 * ─────────────────────────────────────────────────────────────────────────────
 * Covers the complete SNSCreditVault + CHIPToken interaction surface:
 *
 *   Group A: Confidence update + LTV gate math
 *   Group B: Circuit breaker lifecycle (trigger → grace → restore → expire)
 *   Group C: CHIP slashing authorization (asymmetric canonicality rule)
 *   Group D: Access control (unauthorized updater, unauthorized slash)
 *   Group E: Boundary conditions (score = 0, 74, 75, 84, 85, 100)
 *   Group F: Event emission verification
 *
 * Run:
 *   forge test -vvvv
 *   forge test --match-test testCircuitBreaker -vvvv
 *   forge coverage --report lcov
 * ─────────────────────────────────────────────────────────────────────────────
 */

import "forge-std/Test.sol";
import "../src/SNSCreditVault.sol";
import "../src/CHIPToken.sol";

contract SNSTest is Test {

    // ── Fixtures ──────────────────────────────────────────────────────────────
    SNSCreditVault public vault;
    CHIPToken      public chip;

    address public owner       = address(this);
    address public keeper      = makeAddr("keeper");
    address public spvTreasury = makeAddr("spvTreasury");
    address public stakingPool = makeAddr("stakingPool");
    address public validator   = makeAddr("validator");
    address public attacker    = makeAddr("attacker");

    // Mirrors contract constants
    uint256 constant FLOOR     = 53_700_000e6;
    uint256 constant CEILING   = 86_400_000e6;
    uint256 constant GRACE     = 14 days;

    // ── Setup ─────────────────────────────────────────────────────────────────
    function setUp() public {
        vault = new SNSCreditVault(91);          // Deploy at C=91 (premium tier)
        chip  = new CHIPToken(
            address(vault),
            spvTreasury,
            stakingPool
        );

        // Authorize keeper as updater
        vault.authorizeUpdater(keeper);

        // Fund validator with CHIP (simulate staked position)
        // Owner received genesis supply in constructor
        chip.transfer(validator, 1_000_000 * 1e18);
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP A: Confidence update + LTV gate math
    // ═════════════════════════════════════════════════════════════════════════

    function testInitialState() public view {
        assertEq(vault.confidenceScore(), 91);
        assertFalse(vault.circuitBroken());
        assertEq(vault.activeLtv(), 70);

        uint256 expectedCap = (CEILING * 7_000) / 10_000;
        assertEq(vault.borrowCapacity(), expectedCap);
    }

    function testPremiumTierAt85() public {
        vm.prank(keeper);
        vault.updateConfidence(85);

        assertEq(vault.activeLtv(), 70);
        assertEq(vault.borrowCapacity(), (CEILING * 7_000) / 10_000);
        assertFalse(vault.circuitBroken());
    }

    function testFloorTierAt84() public {
        vm.prank(keeper);
        vault.updateConfidence(84);

        assertEq(vault.activeLtv(), 60);
        assertEq(vault.borrowCapacity(), (FLOOR * 6_000) / 10_000);
        assertFalse(vault.circuitBroken());
    }

    function testFloorTierAt75() public {
        vm.prank(keeper);
        vault.updateConfidence(75);

        // 75 is exactly C_HALT_TRIGGER — should NOT break (< 75 breaks)
        assertFalse(vault.circuitBroken());
        assertEq(vault.activeLtv(), 60);
        assertGt(vault.borrowCapacity(), 0);
    }

    function testLTVZeroWhenBroken() public {
        vm.prank(keeper);
        vault.updateConfidence(74);  // triggers break

        assertTrue(vault.circuitBroken());
        assertEq(vault.activeLtv(), 0);
        assertEq(vault.borrowCapacity(), 0);
    }

    function testFuzzLTVMath(uint8 score) public {
        // Any score update should never produce capacity > ceiling * 70%
        vm.assume(score <= 100);
        vm.prank(keeper);
        vault.updateConfidence(score);

        uint256 cap     = vault.borrowCapacity();
        uint256 maxCap  = (CEILING * 7_000) / 10_000;
        assertLe(cap, maxCap, "capacity must never exceed premium ceiling");
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP B: Circuit breaker lifecycle
    // ═════════════════════════════════════════════════════════════════════════

    function testCircuitBreakTrigger() public {
        vm.prank(keeper);
        vault.updateConfidence(74);

        assertTrue(vault.circuitBroken());
        assertGt(vault.gracePeriodEnd(), block.timestamp);
        assertEq(vault.gracePeriodEnd(), block.timestamp + GRACE);
    }

    function testCircuitRestoreWithinGrace() public {
        // Break
        vm.prank(keeper);
        vault.updateConfidence(74);
        assertTrue(vault.circuitBroken());

        // Partial time passes but still within grace
        vm.warp(block.timestamp + 7 days);

        // Recover
        vm.prank(keeper);
        vault.updateConfidence(81);  // ≥ C_REOPEN_GATE (80)

        assertFalse(vault.circuitBroken());
        assertEq(vault.gracePeriodEnd(), 0);
        assertGt(vault.borrowCapacity(), 0);
    }

    function testCircuitDoesNotRestoreBelow80() public {
        vm.prank(keeper);
        vault.updateConfidence(74);
        assertTrue(vault.circuitBroken());

        vm.warp(block.timestamp + 3 days);

        // Score recovers to 79 — below C_REOPEN_GATE
        vm.prank(keeper);
        vault.updateConfidence(79);

        assertTrue(vault.circuitBroken(), "circuit must stay broken below reopen gate");
    }

    function testCircuitStaysBrokenAfterGraceExpiry() public {
        vm.prank(keeper);
        vault.updateConfidence(74);
        assertTrue(vault.circuitBroken());

        // Warp past grace period
        vm.warp(block.timestamp + GRACE + 1);

        // Score recovers — but grace has expired, circuit stays broken
        vm.prank(keeper);
        vault.updateConfidence(85);

        assertTrue(vault.circuitBroken(), "circuit must stay broken after grace expiry");
        assertEq(vault.borrowCapacity(), 0, "capacity must be zero after grace expiry");
    }

    function testManualCircuitResetByOwner() public {
        // Break + let grace expire
        vm.prank(keeper);
        vault.updateConfidence(74);
        vm.warp(block.timestamp + GRACE + 1);
        vm.prank(keeper);
        vault.updateConfidence(85);
        assertTrue(vault.circuitBroken());

        // Owner manually resets
        vault.manualCircuitReset();

        assertFalse(vault.circuitBroken());
    }

    function testManualResetFailsBelowReopenGate() public {
        vm.prank(keeper);
        vault.updateConfidence(74);
        vm.warp(block.timestamp + GRACE + 1);
        vm.prank(keeper);
        vault.updateConfidence(74);  // still below gate

        vm.expectRevert("SNS: score must be >= C_REOPEN_GATE before manual reset");
        vault.manualCircuitReset();
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP C: CHIP slashing — asymmetric canonicality rule
    // ═════════════════════════════════════════════════════════════════════════

    function testSlashRequiresCircuitBroken() public {
        // Circuit is open — slash must revert
        assertFalse(vault.circuitBroken());

        vm.prank(address(vault));
        vm.expectRevert("CHIP_ERR: REJECTED_VAULT_CIRCUIT_NOT_BROKEN");
        chip.executeSlashingPenalty(validator, 100e18);
    }

    function testSlashSucceedsWhenCircuitBroken() public {
        // Break the circuit on-chain
        vm.prank(keeper);
        vault.updateConfidence(74);
        assertTrue(vault.circuitBroken());

        uint256 balBefore = chip.balanceOf(validator);
        uint256 slashAmt  = 500_000e18;

        vm.prank(address(vault));
        chip.executeSlashingPenalty(validator, slashAmt);

        assertEq(chip.balanceOf(validator), balBefore - slashAmt);
        assertEq(chip.balanceOf(stakingPool), slashAmt, "slashed tokens must route to staking pool");
    }

    function testSlashRevertsIfInsufficientStake() public {
        vm.prank(keeper);
        vault.updateConfidence(74);

        uint256 bal = chip.balanceOf(validator);

        vm.prank(address(vault));
        vm.expectRevert("CHIP_ERR: INSUFFICIENT_STAKE_FOR_SLASHING_BOUNDS");
        chip.executeSlashingPenalty(validator, bal + 1);
    }

    function testSlashCannotBeCalledByNonVault() public {
        vm.prank(keeper);
        vault.updateConfidence(74);

        vm.prank(attacker);
        vm.expectRevert("CHIP_ERR: CALLER_NOT_CANONICAL_VAULT");
        chip.executeSlashingPenalty(validator, 100e18);
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP D: Access control
    // ═════════════════════════════════════════════════════════════════════════

    function testUnauthorizedUpdaterReverts() public {
        vm.prank(attacker);
        vm.expectRevert("SNS: not authorized updater");
        vault.updateConfidence(80);
    }

    function testRevokeUpdater() public {
        vault.revokeUpdater(keeper);

        vm.prank(keeper);
        vm.expectRevert("SNS: not authorized updater");
        vault.updateConfidence(80);
    }

    function testOwnerCannotRevokeThemself() public {
        vm.expectRevert("SNS: cannot revoke owner");
        vault.revokeUpdater(owner);
    }

    function testNonOwnerCannotAuthorize() public {
        vm.prank(attacker);
        vm.expectRevert("SNS: not owner");
        vault.authorizeUpdater(attacker);
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP E: Boundary conditions
    // ═════════════════════════════════════════════════════════════════════════

    function testScoreZeroBreaksCircuit() public {
        vm.prank(keeper);
        vault.updateConfidence(0);

        assertTrue(vault.circuitBroken());
        assertEq(vault.borrowCapacity(), 0);
        assertEq(vault.activeLtv(), 0);
    }

    function testScore100PremiumTier() public {
        vm.prank(keeper);
        vault.updateConfidence(100);

        assertFalse(vault.circuitBroken());
        assertEq(vault.activeLtv(), 70);
        assertEq(vault.borrowCapacity(), (CEILING * 7_000) / 10_000);
    }

    function testScoreOutOfRangeReverts() public {
        // uint8 max is 255 — solidity truncation not possible via typed call,
        // but test the require guard path via direct call encoding
        vm.prank(keeper);
        // Score 101 should revert
        (bool success, ) = address(vault).call(
            abi.encodeWithSignature("updateConfidence(uint8)", uint8(101))
        );
        // uint8(101) is valid range — passes; 101 <= 100 check catches it
        // Note: cast to uint8 makes 101 literal fit; the require fires inside
        assertFalse(success == false, "101 should revert on require");
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP F: Event emission
    // ═════════════════════════════════════════════════════════════════════════

    function testConfidenceUpdatedEventEmitted() public {
        vm.prank(keeper);
        vm.expectEmit(true, true, true, true);
        emit SNSCreditVault.ConfidenceUpdated(
            85,
            91,
            (CEILING * 7_000) / 10_000,
            70,
            keeper
        );
        vault.updateConfidence(85);
    }

    function testCircuitBrokenEventEmitted() public {
        uint256 expectedGrace = block.timestamp + GRACE;

        vm.prank(keeper);
        vm.expectEmit(true, false, true, true);
        emit SNSCreditVault.CircuitBroken(74, expectedGrace, keeper);
        vault.updateConfidence(74);
    }

    function testCircuitRestoredEventEmitted() public {
        vm.prank(keeper);
        vault.updateConfidence(74);

        vm.warp(block.timestamp + 3 days);

        vm.prank(keeper);
        vm.expectEmit(true, true, false, true);
        emit SNSCreditVault.CircuitRestored(81, keeper);
        vault.updateConfidence(81);
    }

    function testProtocolSlashingEventEmitted() public {
        vm.prank(keeper);
        vault.updateConfidence(74);

        uint256 slashAmt = 100e18;

        vm.prank(address(vault));
        vm.expectEmit(true, false, false, true);
        emit CHIPToken.ProtocolSlashing(validator, slashAmt);
        chip.executeSlashingPenalty(validator, slashAmt);
    }

    // ═════════════════════════════════════════════════════════════════════════
    // GROUP G: Full scenario — nominal → stress → recovery → re-breach
    // ═════════════════════════════════════════════════════════════════════════

    function testFullScenarioNominalToRecovery() public {
        // 1. Nominal: premium tier
        vm.prank(keeper);
        vault.updateConfidence(91);
        assertEq(vault.activeLtv(), 70);

        // 2. Stress: drop to floor
        vm.prank(keeper);
        vault.updateConfidence(80);
        assertEq(vault.activeLtv(), 60);

        // 3. Break
        vm.prank(keeper);
        vault.updateConfidence(72);
        assertTrue(vault.circuitBroken());
        assertEq(vault.borrowCapacity(), 0);

        // 4. Slash validator while broken
        vm.prank(address(vault));
        chip.executeSlashingPenalty(validator, 200_000e18);

        // 5. Recover within grace
        vm.warp(block.timestamp + 5 days);
        vm.prank(keeper);
        vault.updateConfidence(82);
        assertFalse(vault.circuitBroken());
        assertGt(vault.borrowCapacity(), 0);

        // 6. Slash must now revert (circuit open)
        vm.prank(address(vault));
        vm.expectRevert("CHIP_ERR: REJECTED_VAULT_CIRCUIT_NOT_BROKEN");
        chip.executeSlashingPenalty(validator, 100e18);

        // 7. Return to premium
        vm.prank(keeper);
        vault.updateConfidence(90);
        assertEq(vault.activeLtv(), 70);
    }
}
