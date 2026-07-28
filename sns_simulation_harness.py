#!/usr/bin/env python3
"""
sns_simulation_harness.py — Multi-Oracle ECDSA Simulation Harness
─────────────────────────────────────────────────────────────────────────────
Three independent oracle keypairs each sign a confidence score.
The harness aggregates to a median, then:

  1. POSTs median to server.js  (off-chain mirror — fast path)
  2. Broadcasts signed raw tx to Anvil via eth_sendRawTransaction
     (on-chain canonical — SNSCreditVault.updateConfidence)

Oracle → feed mapping:
  oracle_0  Chainlink  (±2 noise)
  oracle_1  Pyth       (±2 noise)
  oracle_2  ZK Audit   (deterministic, zero noise)

Usage:
  pip install eth-account web3 requests rich python-dotenv
  python sns_simulation_harness.py               # all scenarios, live
  python sns_simulation_harness.py --dry         # no network calls
  python sns_simulation_harness.py --scenario CIRCUIT_BREAK

Required ENV (.env):
  SNS_INTERNAL_SECRET     Off-chain API auth key
  KEEPER_PRIVATE_KEY      EOA authorized on SNSCreditVault
  VAULT_ADDRESS           Deployed contract address
  RPC_URL                 http://127.0.0.1:8545 (Anvil default)
  SNS_API_URL             http://localhost:3001/api/sns/update-telemetry
─────────────────────────────────────────────────────────────────────────────
"""

import os
import sys
import time
import json
import random
import argparse
from dataclasses import dataclass
from typing import Optional

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

load_dotenv()

# ── Optional Web3 import ──────────────────────────────────────────────────────
try:
    from eth_account import Account
    from eth_account.messages import encode_defunct
    from web3 import Web3
    WEB3_OK = True
except ImportError:
    WEB3_OK = False

console = Console()

# ── Environment ───────────────────────────────────────────────────────────────
API_URL    = os.getenv("SNS_API_URL",           "http://localhost:3001/api/sns/update-telemetry")
SECRET     = os.getenv("SNS_INTERNAL_SECRET",   "dev_secret")
KEEPER_PK  = os.getenv("KEEPER_PRIVATE_KEY",    "")
VAULT_ADDR = os.getenv("VAULT_ADDRESS",          "")
RPC_URL    = os.getenv("RPC_URL",                "http://127.0.0.1:8545")
BAD_NODE   = os.getenv("MALICIOUS_NODE_MOCK",    "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC")
STEP_DELAY = float(os.getenv("STEP_DELAY_SEC",  "1.0"))

# ── Anvil test keypairs (deterministic — NEVER use in production) ─────────────
ORACLE_KEYS = [
    "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",  # Anvil #0
    "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",  # Anvil #1
    "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",  # Anvil #2
]
ORACLE_NAMES = ["CHAINLINK", "PYTH", "ZK_AUDIT"]

# ── Minimal vault ABI ─────────────────────────────────────────────────────────
VAULT_ABI = [
    {
        "inputs": [{"internalType": "uint8", "name": "newScore", "type": "uint8"}],
        "name": "updateConfidence",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "confidenceScore",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "circuitBroken",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# ── Scenarios ─────────────────────────────────────────────────────────────────
SCENARIOS = {
    "NOMINAL": {
        "description": "Sustained premium tier — Levers 1+2 deployed",
        "steps": [
            {"base": 86, "knowns": 12, "unknowns": 2},
            {"base": 88, "knowns": 13, "unknowns": 1},
            {"base": 91, "knowns": 14, "unknowns": 1},
            {"base": 93, "knowns": 15, "unknowns": 1},
            {"base": 94, "knowns": 15, "unknowns": 0},
        ],
    },
    "FLOOR_STRESS": {
        "description": "Oscillation at floor threshold — 60% LTV locked",
        "steps": [
            {"base": 84, "knowns": 10, "unknowns": 4},
            {"base": 81, "knowns": 9,  "unknowns": 5},
            {"base": 78, "knowns": 8,  "unknowns": 6},
            {"base": 76, "knowns": 7,  "unknowns": 7},
            {"base": 75, "knowns": 7,  "unknowns": 7},
            {"base": 77, "knowns": 8,  "unknowns": 6},
            {"base": 80, "knowns": 9,  "unknowns": 5},
        ],
    },
    "CIRCUIT_BREAK": {
        "description": "Hard drop → circuit fires → CHIP slashing event",
        "steps": [
            {"base": 85, "knowns": 12, "unknowns": 2},
            {"base": 78, "knowns": 9,  "unknowns": 5},
            {"base": 73, "knowns": 6,  "unknowns": 8, "slash": True},
            {"base": 68, "knowns": 4,  "unknowns": 10, "slash": True},
            {"base": 65, "knowns": 3,  "unknowns": 11, "slash": True},
            {"base": 71, "knowns": 5,  "unknowns": 9},
            {"base": 75, "knowns": 7,  "unknowns": 7},
        ],
    },
    "RECOVERY": {
        "description": "Reflex loops activate — floor → premium",
        "steps": [
            {"base": 76, "knowns": 8,  "unknowns": 6},
            {"base": 79, "knowns": 9,  "unknowns": 5},
            {"base": 81, "knowns": 10, "unknowns": 4},
            {"base": 84, "knowns": 11, "unknowns": 3},
            {"base": 85, "knowns": 13, "unknowns": 2},
            {"base": 88, "knowns": 14, "unknowns": 1},
        ],
    },
    "DIVERGENT": {
        "description": "Oracle feeds diverge — median safety net stress test",
        "steps": [
            {"base": 85, "spread": 14},  # CL~92, PYTH~78, ZK=85 → median 85
            {"base": 82, "spread": 16},  # CL~90, PYTH~74, ZK=82 → median 82
            {"base": 78, "spread": 20},  # CL~88, PYTH~68, ZK=78 → median 78
            {"base": 74, "spread": 22},  # CL~85, PYTH~63, ZK=74 → median 74 BREAK
        ],
    },
}

# ── Oracle feed ───────────────────────────────────────────────────────────────
@dataclass
class OracleFeed:
    name: str
    private_key: str
    score: int = 91
    signature: str = ""
    address: str = ""

    def sign(self, score: int) -> "OracleFeed":
        self.score = max(0, min(100, score))
        if not WEB3_OK:
            import hashlib
            h = hashlib.sha256(f"{self.name}:{score}".encode()).hexdigest()
            self.signature = f"0x{h[:64]}"
            self.address   = "0x" + "0" * 40
            return self
        msg    = encode_defunct(text=f"SNS_CONFIDENCE:{score}")
        signed = Account.sign_message(msg, private_key=self.private_key)
        self.signature = signed.signature.hex()
        self.address   = Account.from_key(self.private_key).address
        return self

# ── Multi-oracle aggregation ──────────────────────────────────────────────────
def aggregate(base_score: int, spread: int = 4) -> tuple[int, list[OracleFeed]]:
    """
    Each feed independently scores with noise. ZK feed is deterministic.
    Returns (median_score, signed_feeds).
    Spread > 10 tests the manipulation-resistance of the median.
    """
    feeds = [OracleFeed(ORACLE_NAMES[i], ORACLE_KEYS[i]) for i in range(3)]
    scores = []
    for i, feed in enumerate(feeds):
        noise = 0 if i == 2 else random.randint(-(spread // 2), spread // 2)
        feed.sign(base_score + noise)
        scores.append(feed.score)

    scores_sorted = sorted(scores)
    median = scores_sorted[1]  # middle value — manipulation resistant
    return median, feeds

# ── On-chain broadcast ────────────────────────────────────────────────────────
def broadcast_on_chain(score: int, dry: bool) -> Optional[str]:
    if dry:
        return f"0x{'d47y' * 16}"[:66]

    if not WEB3_OK:
        console.print("  [yellow][ON-CHAIN SKIP][/] eth-account/web3 not installed.")
        return None

    if not KEEPER_PK or not VAULT_ADDR:
        console.print("  [yellow][ON-CHAIN SKIP][/] KEEPER_PRIVATE_KEY or VAULT_ADDRESS not set.")
        return None

    try:
        w3      = Web3(Web3.HTTPProvider(RPC_URL))
        account = Account.from_key(KEEPER_PK)
        vault   = w3.eth.contract(
            address=Web3.to_checksum_address(VAULT_ADDR),
            abi=VAULT_ABI,
        )

        nonce   = w3.eth.get_transaction_count(account.address)
        fn      = vault.functions.updateConfidence(score)
        gas_est = fn.estimate_gas({"from": account.address})

        raw_tx = fn.build_transaction({
            "from":     account.address,
            "nonce":    nonce,
            "gas":      int(gas_est * 1.25),
            "gasPrice": w3.eth.gas_price,
            "chainId":  w3.eth.chain_id,
        })

        signed  = account.sign_transaction(raw_tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=15)

        status  = "✅ CONFIRMED" if receipt.status == 1 else "❌ REVERTED"
        console.print(
            f"  [green][ON-CHAIN][/] {status} | "
            f"block {receipt.blockNumber} | gas {receipt.gasUsed} | "
            f"{tx_hash.hex()[:20]}..."
        )
        return tx_hash.hex()

    except Exception as exc:
        console.print(f"  [red][ON-CHAIN ERROR][/] {exc}")
        return None

# ── Off-chain API injection ───────────────────────────────────────────────────
def inject_off_chain(median: int, step: dict, brief_id: str, dry: bool) -> dict:
    payload = {
        "secretKey":      SECRET,
        "newConfidence":  median,
        "newKnowns":      step.get("knowns", 8),
        "newUnknowns":    step.get("unknowns", 3),
        "briefId":        brief_id,
        "forceBroadcast": step.get("slash", False),
        "maliciousNode":  BAD_NODE if step.get("slash") else None,
        "slashAmount":    2500 if step.get("slash") else 0,
    }
    if dry:
        ltv = 70 if median >= 85 else 60 if median >= 75 else 0
        return {"_dry": True, "state": {"activeLtv": ltv, "borrowCapacity": 0 if ltv == 0 else 1}}

    try:
        r = requests.post(API_URL, json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"_offline": True}
    except Exception as exc:
        return {"_error": str(exc)}

# ── LTV formatting ────────────────────────────────────────────────────────────
def ltv_fmt(score: int) -> str:
    if score < 75: return "[red bold]BROKEN  0%[/]"
    if score < 85: return "[yellow]FLOOR  60%[/]"
    return "[green]PREMIUM 70%[/]"

# ── Scenario runner ───────────────────────────────────────────────────────────
def run_scenario(name: str, cfg: dict, dry: bool, counter: list[int]) -> None:
    console.print(Panel(
        f"[bold yellow]{name}[/]\n[dim]{cfg['description']}[/]",
        border_style="yellow", box=box.DOUBLE_EDGE,
    ))

    table = Table(
        "Step", "CL Score", "PYTH Score", "ZK Score",
        "Median", "LTV Gate", "API", "On-Chain TX",
        box=box.SIMPLE_HEAD, header_style="bold yellow", style="dim",
    )

    for i, step in enumerate(cfg["steps"]):
        spread   = step.get("spread", 4)
        brief_id = f"B-{counter[0]:04d}"
        counter[0] += 1

        median, feeds = aggregate(step["base"], spread=spread)

        # Format feed columns
        def feed_col(f: OracleFeed) -> str:
            c = "green" if f.score >= 85 else "yellow" if f.score >= 75 else "red"
            return f"[{c}]{f.score:02d}[/] [dim]{f.signature[:8]}…[/]"

        # Off-chain injection
        api_res = inject_off_chain(median, step, brief_id, dry=dry)
        if "_offline" in api_res:   api_note = "[dim]OFFLINE[/]"
        elif "_error" in api_res:   api_note = "[red]ERR[/]"
        elif "_dry" in api_res:     api_note = "[dim]DRY ✓[/]"
        else:                       api_note = "[green]✓ ACK[/]"

        # On-chain broadcast: always on slash events, circuit breaks, and step 0
        should_cast = step.get("slash") or median < 75 or i == 0
        tx = broadcast_on_chain(median, dry=dry) if should_cast else None
        tx_note = f"[green]{(tx or '')[:16]}…[/]" if tx else "[dim]—[/]"

        table.add_row(
            str(i + 1),
            feed_col(feeds[0]), feed_col(feeds[1]), feed_col(feeds[2]),
            f"[bold]0.{median:02d}[/]",
            ltv_fmt(median),
            api_note,
            tx_note,
        )

        if step.get("slash"):
            console.print(
                f"  [red bold]▼ SLASH EVENT[/]  Circuit broken. "
                f"CHIP slashing authorized against {BAD_NODE[:18]}…"
            )
        if median < 75 and not step.get("slash"):
            console.print(f"  [red]▼ CIRCUIT BREAK[/]  C=0.{median} < 0.75 threshold.")

        time.sleep(STEP_DELAY)

    console.print(table)
    console.print()

# ── Summary ───────────────────────────────────────────────────────────────────
def summary(dry: bool) -> None:
    mode = "[yellow]DRY RUN[/]" if dry else "[green]LIVE[/]"
    w3   = "[green]OK[/]" if WEB3_OK else "[yellow]NOT INSTALLED — pip install eth-account web3[/]"
    console.print(Panel(
        f"[bold yellow]HARNESS COMPLETE[/]  Mode: {mode}  Web3: {w3}\n\n"
        "[bold]Canonicality rule enforced:[/]\n"
        "  Node proposes (off-chain API) → Chain disposes (on-chain vault)\n"
        "  CHIP slashing only when vault.circuitBroken() == true (on-chain)\n\n"
        "[bold]Oracle architecture:[/]\n"
        f"  CHAINLINK  key {ORACLE_KEYS[0][:20]}…  (±2 noise)\n"
        f"  PYTH       key {ORACLE_KEYS[1][:20]}…  (±2 noise)\n"
        f"  ZK_AUDIT   key {ORACLE_KEYS[2][:20]}…  (deterministic)\n"
        "  Median of 3 feeds prevents single-feed manipulation.\n\n"
        "[bold]Verify on-chain state:[/]\n"
        "  cast call $VAULT_ADDRESS 'confidenceScore()(uint8)'\n"
        "  cast call $VAULT_ADDRESS 'circuitBroken()(bool)'\n"
        "  forge test -vvvv",
        border_style="yellow", box=box.DOUBLE_EDGE,
    ))

# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SNS Multi-Oracle Simulation Harness")
    parser.add_argument("--dry",      action="store_true",
                        help="Validate logic without any network calls")
    parser.add_argument("--scenario", default="ALL",
                        help=f"Scenario or ALL. Options: {', '.join(SCENARIOS)}")
    args = parser.parse_args()

    console.print(Panel(
        "[bold yellow]SNS MULTI-ORACLE SIMULATION HARNESS[/]\n"
        "[dim]ECDSA-signed oracle feeds → median aggregation → raw tx broadcast[/]\n"
        f"[dim]API:      {API_URL}[/]\n"
        f"[dim]Chain:    {RPC_URL}[/]\n"
        f"[dim]Vault:    {VAULT_ADDR or '(not set)'}[/]\n"
        f"[dim]Web3:     {'available' if WEB3_OK else 'not installed'}[/]",
        border_style="yellow",
    ))

    if not WEB3_OK:
        console.print(
            "[yellow]⚠  eth-account / web3 not installed — on-chain broadcast disabled.[/]\n"
            "[dim]   pip install eth-account web3[/]\n"
        )

    if args.scenario == "ALL":
        targets = SCENARIOS
    elif args.scenario in SCENARIOS:
        targets = {args.scenario: SCENARIOS[args.scenario]}
    else:
        console.print(f"[red]Unknown scenario: {args.scenario}[/]")
        sys.exit(1)

    counter = [54]  # mutable brief ID counter
    for name, cfg in targets.items():
        run_scenario(name, cfg, dry=args.dry, counter=counter)

    summary(dry=args.dry)
