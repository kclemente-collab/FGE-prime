-- FGE-SPEC-LAYERED-FASHION-DB-001 v0.2.0
-- Layered Fashion Module — PostgreSQL 15+ DDL
-- Status: SPEC_CANDIDATE / NOT_CANON_PROMOTED
-- Canon effect: NONE
-- Parent: FGE-SYS-MODULAR-FASHION-OS-001
--
-- Authority:
--   digital_assets_registry     = commercial + identity ledger
--   fabric_master_profiles      = physical constants (Storage)
--   fabric_description_index    = FDE lookup (UI + viewport)
--   clipping_occlusion_rules    = layer stack + hollow-out
--   asset_customization_hub     = tint / pattern overlays (Display)
--   asset_valuation_event       = append-only valuation / royalty evidence
--   fare_*                      = runtime evidence only (not product truth)
--
-- Engine-specific Chaos / Substrate / AmmoJS payloads are NOT stored as
-- identity. Persist them as Adapter JSON documents keyed by asset_id.
--
-- FARE (Fashion Asset Runtime Evidence) tables record what a runtime DID.
-- They do not own SKU identity. Soft-link via sku_identifier /
-- garment_runtime_id. No ON DELETE CASCADE into the product registry.
-- fare_runtime_frame is a serialization packet, not a table.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------------
-- 1. Core Digital Asset Registry
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS digital_assets_registry (
    asset_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku_identifier VARCHAR(64) UNIQUE NOT NULL,
    brand_name VARCHAR(100) NOT NULL,
    rarity_tier VARCHAR(32) NOT NULL
        CHECK (rarity_tier IN ('Haute_Couture', 'Premium', 'Street_Drop')),
    interoperability_tokens TEXT[] NOT NULL DEFAULT '{}',
    digital_rights_framework JSONB NOT NULL DEFAULT '{}'::jsonb,
    envelope_object_id VARCHAR(128),
    envelope_version VARCHAR(32),
    status VARCHAR(64) NOT NULL DEFAULT 'SPEC_CANDIDATE',
    canon_effect VARCHAR(32) NOT NULL DEFAULT 'NONE'
        CHECK (canon_effect IN ('NONE', 'PROPOSED', 'AUTHORIZED', 'LOCKED')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_digital_assets_brand
    ON digital_assets_registry (brand_name);
CREATE INDEX IF NOT EXISTS idx_digital_assets_rarity
    ON digital_assets_registry (rarity_tier);

-- ---------------------------------------------------------------------------
-- 2. Fabric Description Index (FDE static registry)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fabric_description_index (
    global_fabric_id VARCHAR(64) PRIMARY KEY,
    display_name_en VARCHAR(160) NOT NULL,
    tactile_description TEXT NOT NULL,
    use_raytracing_anisotropy BOOLEAN NOT NULL DEFAULT FALSE,
    parallax_occlusion_mapping_depth FLOAT,
    clear_coat_present BOOLEAN NOT NULL DEFAULT FALSE,
    localization_manifest JSONB NOT NULL DEFAULT '{}'::jsonb,
    -- Governing representation: extensible UI metadata stays one JSON object.
    -- Do not duplicate individual anchor keys as independently writable columns.
    display_ui_anchors JSONB NOT NULL DEFAULT '{}'::jsonb
        CHECK (jsonb_typeof(display_ui_anchors) = 'object'),
    viewport_rendering_overrides JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- 3. Master Fabric Physical Reference + UE5-neutral constants
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fabric_master_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL
        REFERENCES digital_assets_registry(asset_id) ON DELETE CASCADE,
    global_fabric_id VARCHAR(64) NOT NULL
        REFERENCES fabric_description_index(global_fabric_id),
    mass_per_unit_area FLOAT NOT NULL CHECK (mass_per_unit_area > 0),
    bending_stiffness FLOAT NOT NULL,
    stretching_stiffness FLOAT NOT NULL,
    shearing_stiffness FLOAT,
    friction_coefficient FLOAT NOT NULL CHECK (friction_coefficient BETWEEN 0 AND 1),
    substrate_shading_topology VARCHAR(64) NOT NULL DEFAULT 'Substrate_Slab_Blended',
    physical_intent JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fabric_profiles_asset
    ON fabric_master_profiles (asset_id);
CREATE INDEX IF NOT EXISTS idx_fabric_profiles_fabric
    ON fabric_master_profiles (global_fabric_id);

-- ---------------------------------------------------------------------------
-- 4. Layer stacking + deactivation logic
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clipping_occlusion_rules (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL
        REFERENCES digital_assets_registry(asset_id) ON DELETE CASCADE,
    z_layer_index INTEGER NOT NULL CHECK (z_layer_index BETWEEN 0 AND 100),
    layer_class VARCHAR(32),
    deactivation_zones_skin TEXT[] NOT NULL DEFAULT '{}',
    deactivation_zones_sub_layers INTEGER[] NOT NULL DEFAULT '{}',
    push_out_distance_mm FLOAT NOT NULL DEFAULT 2.5,
    collision_channel VARCHAR(128) DEFAULT 'ECC_GameTraceChannel_ClothingInteraction',
    normal_offset_falloff_power FLOAT DEFAULT 1.2,
    alpha_mask_registry JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_clipping_asset
    ON clipping_occlusion_rules (asset_id);
CREATE INDEX IF NOT EXISTS idx_clipping_z
    ON clipping_occlusion_rules (z_layer_index);

-- ---------------------------------------------------------------------------
-- 5. Dynamic customization blueprint
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS asset_customization_hub (
    customization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL
        REFERENCES digital_assets_registry(asset_id) ON DELETE CASCADE,
    tint_mask_channel_mappings JSONB NOT NULL DEFAULT '{}'::jsonb,
    max_pattern_tiling_scale FLOAT NOT NULL DEFAULT 1.0,
    allowed_procedural_effects TEXT[] NOT NULL DEFAULT '{}',
    runtime_customization_parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_customization_asset
    ON asset_customization_hub (asset_id);

-- ---------------------------------------------------------------------------
-- 6. Adapter payload vault (engine-specific, downstream of intent)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS asset_adapter_payloads (
    adapter_row_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL
        REFERENCES digital_assets_registry(asset_id) ON DELETE CASCADE,
    target_environment VARCHAR(64) NOT NULL,
    rig_retargeting_profile VARCHAR(128),
    physics_solver VARCHAR(64),
    payload JSONB NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'CANDIDATE',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (asset_id, target_environment)
);

CREATE INDEX IF NOT EXISTS idx_adapter_asset
    ON asset_adapter_payloads (asset_id);

-- ---------------------------------------------------------------------------
-- 7. Append-only commercial valuation evidence
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS asset_valuation_event (
    valuation_event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL
        REFERENCES digital_assets_registry(asset_id) ON DELETE CASCADE,
    event_type VARCHAR(32) NOT NULL
        CHECK (event_type IN ('LIST', 'TRANSFER', 'RENTAL', 'CUSTOMIZATION', 'ROYALTY_ACCRUAL')),
    currency CHAR(3) NOT NULL,
    gross_value_minor BIGINT NOT NULL CHECK (gross_value_minor >= 0),
    royalty_bps INTEGER NOT NULL CHECK (royalty_bps BETWEEN 0 AND 10000),
    royalty_distribution JSONB NOT NULL DEFAULT '[]'::jsonb,
    platform VARCHAR(64) NOT NULL,
    license_id VARCHAR(128) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_asset_valuation_asset
    ON asset_valuation_event (asset_id, created_at);

-- ---------------------------------------------------------------------------
-- 8. Seed FDE row used by the non-canon example coat
-- ---------------------------------------------------------------------------
INSERT INTO fabric_description_index (
    global_fabric_id,
    display_name_en,
    tactile_description,
    use_raytracing_anisotropy,
    parallax_occlusion_mapping_depth,
    clear_coat_present,
    localization_manifest,
    display_ui_anchors,
    viewport_rendering_overrides
) VALUES (
    'fab_lthr_nappa_01',
    'Premium Heavy Nappa Leather',
    'Thick, full-grain milled leather with a semi-matte sheen and pronounced structure.',
    TRUE,
    0.02,
    FALSE,
    jsonb_build_object(
        'display_name_en', 'Premium Heavy Nappa Leather',
        'tactile_description', 'Thick, full-grain milled leather with a semi-matte sheen and pronounced structure.'
    ),
    jsonb_build_object(
        'icon_thumbnail_uri', 's3://ui/fabric-swatches/nappa_leather_thumb.png',
        'sound_profile_on_movement', 'sfx_leather_rustle_low_freq'
    ),
    jsonb_build_object(
        'use_raytracing_anisotropy', TRUE,
        'parallax_occlusion_mapping_depth', 0.02,
        'clear_coat_present', FALSE
    )
)
ON CONFLICT (global_fabric_id) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 9. FARE evidence ledger
--     Object: FGE-FARE-SERIALIZATION-LEDGER-001
--     Version: 0.6.1
--     Status: REVIEWED_CANDIDATE_ARCHITECTURE
--     Canon effect: NONE
--     Parent: FGE-SPEC-LAYERED-FASHION-DB-001
--
--     Emulated by sandboxes/FGE-FARE-v0.6-serialization-ledger.html
--     Tables: fare_asset_identity, fare_mutation_attempt,
--             fare_validation_event, fare_recovery_event,
--             fare_validated_checkpoint, fare_provenance_event
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fare_asset_identity (
    identity_row_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garment_runtime_id VARCHAR(64) NOT NULL,
    sku_identifier VARCHAR(64) NOT NULL,
    display_name VARCHAR(160) NOT NULL,
    z_layer_index INTEGER NOT NULL CHECK (z_layer_index BETWEEN 0 AND 100),
    brand_name VARCHAR(100) NOT NULL,
    fit_envelope JSONB NOT NULL DEFAULT '{}'::jsonb,
    rights_policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    body_zones TEXT[] NOT NULL DEFAULT '{}',
    source_asset_id UUID
        REFERENCES digital_assets_registry(asset_id) ON DELETE SET NULL,
    status VARCHAR(64) NOT NULL DEFAULT 'SPEC_CANDIDATE',
    canon_effect VARCHAR(32) NOT NULL DEFAULT 'NONE'
        CHECK (canon_effect IN ('NONE', 'PROPOSED', 'AUTHORIZED', 'LOCKED')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (garment_runtime_id)
);

CREATE INDEX IF NOT EXISTS idx_fare_identity_sku
    ON fare_asset_identity (sku_identifier);
CREATE INDEX IF NOT EXISTS idx_fare_identity_source
    ON fare_asset_identity (source_asset_id);

CREATE TABLE IF NOT EXISTS fare_mutation_attempt (
    attempt_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garment_runtime_id VARCHAR(64) NOT NULL,
    sku_identifier VARCHAR(64) NOT NULL,
    session_id VARCHAR(64) NOT NULL,
    frame_sequence_id BIGINT,
    scenario_id VARCHAR(16),
    mutation_kind VARCHAR(32) NOT NULL
        CHECK (mutation_kind IN (
            'TINT',
            'MATERIAL_SUBSTITUTION',
            'FIT_MORPH',
            'PLATFORM',
            'RIGHTS_STATE',
            'OTHER'
        )),
    requested_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    authorized BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fare_mutation_sku
    ON fare_mutation_attempt (sku_identifier);
CREATE INDEX IF NOT EXISTS idx_fare_mutation_session
    ON fare_mutation_attempt (session_id, created_at);

CREATE TABLE IF NOT EXISTS fare_validation_event (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garment_runtime_id VARCHAR(64) NOT NULL,
    sku_identifier VARCHAR(64) NOT NULL,
    session_id VARCHAR(64) NOT NULL,
    frame_sequence_id BIGINT,
    scenario_id VARCHAR(16),
    gate_name VARCHAR(32) NOT NULL
        CHECK (gate_name IN ('FIT', 'RIGHTS', 'PLATFORM', 'STABILITY', 'IDENTITY')),
    gate_code VARCHAR(32) NOT NULL
        CHECK (gate_code IN ('PASS', 'ADAPT', 'REJECT', 'DENY', 'RECOVERED', 'FAIL')),
    error_code_namespace VARCHAR(128) NOT NULL DEFAULT 'NONE',
    classification VARCHAR(32) NOT NULL DEFAULT 'NONE'
        CHECK (classification IN ('NONE', 'RECOVERABLE', 'TERMINAL')),
    final_state_disposition VARCHAR(64),
    frame_integrity_safe BOOLEAN NOT NULL DEFAULT FALSE,
    detail JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fare_validation_session
    ON fare_validation_event (session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_fare_validation_gate
    ON fare_validation_event (gate_name, gate_code);

CREATE TABLE IF NOT EXISTS fare_recovery_event (
    recovery_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garment_runtime_id VARCHAR(64),
    sku_identifier VARCHAR(64),
    session_id VARCHAR(64) NOT NULL,
    frame_sequence_id BIGINT,
    scenario_id VARCHAR(16),
    recovery_action VARCHAR(64) NOT NULL
        CHECK (recovery_action IN (
            'RESTORE_AUTHORIZED_DEFAULT',
            'ROLLBACK_MATERIAL',
            'REJECT_GARMENT',
            'TERMINATE_ASSET',
            'FAIL_CLOSED',
            'QUARANTINE',
            'RESTART_REVERIFY',
            'ROLLBACK_PREV_LKG'
        )),
    cycles_consumed INTEGER NOT NULL DEFAULT 1
        CHECK (cycles_consumed >= 0),
    lkg_hash VARCHAR(128),
    detail JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fare_recovery_session
    ON fare_recovery_event (session_id, created_at);

CREATE TABLE IF NOT EXISTS fare_validated_checkpoint (
    checkpoint_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(64) NOT NULL,
    frame_sequence_id BIGINT NOT NULL,
    cryptographic_ledger_hash VARCHAR(128) NOT NULL,
    previous_hash VARCHAR(128),
    authority_classification VARCHAR(64) NOT NULL DEFAULT 'VALIDATED_RUNTIME_EVIDENCE'
        CHECK (authority_classification IN (
            'VALIDATED_RUNTIME_EVIDENCE',
            'PROVISIONAL_ROLLBACK'
        )),
    composition_envelope JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_fare_checkpoint_active_session
    ON fare_validated_checkpoint (session_id)
    WHERE is_active;
CREATE INDEX IF NOT EXISTS idx_fare_checkpoint_hash
    ON fare_validated_checkpoint (cryptographic_ledger_hash);

CREATE TABLE IF NOT EXISTS fare_provenance_event (
    provenance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(64) NOT NULL,
    frame_sequence_id BIGINT,
    previous_hash VARCHAR(128),
    current_hash VARCHAR(128) NOT NULL,
    document_status VARCHAR(64) NOT NULL DEFAULT 'REVIEWED_CANDIDATE_ARCHITECTURE',
    reference_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    canon_effect VARCHAR(32) NOT NULL DEFAULT 'NONE'
        CHECK (canon_effect IN ('NONE', 'PROPOSED', 'AUTHORIZED', 'LOCKED')),
    execution_authority VARCHAR(32) NOT NULL DEFAULT 'CANDIDATE',
    v6_lkg_reverify BOOLEAN NOT NULL DEFAULT FALSE,
    event_kind VARCHAR(32) NOT NULL DEFAULT 'FRAME_COMMIT'
        CHECK (event_kind IN (
            'FRAME_COMMIT',
            'RECOVERY_APPEND',
            'RESTART_REVERIFY',
            'ROLLBACK'
        )),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fare_provenance_session
    ON fare_provenance_event (session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_fare_provenance_hash
    ON fare_provenance_event (current_hash);

-- fare_runtime_frame is the v0.6 serialization packet emitted by the sandbox.
-- Persist packets as fare_provenance_event.payload or an Adapter JSON document.
-- Do not create a mutable product table for frames.

COMMIT;
