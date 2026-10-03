import os
from pathlib import Path
import unittest


DATABASE_URL = os.environ.get("FGE_TEST_DATABASE_URL")


@unittest.skipUnless(DATABASE_URL, "FGE_TEST_DATABASE_URL not configured")
class PostgreSQLIntegrationTest(unittest.TestCase):
    def test_schema_fde_rights_and_valuation_round_trip(self):
        import psycopg

        sql_path = Path(__file__).resolve().parents[1] / "schema" / "layered_fashion_module.sql"
        with psycopg.connect(DATABASE_URL, autocommit=True) as connection:
            connection.execute(sql_path.read_text())
            fde_columns = {
                row[0]
                for row in connection.execute(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_name = 'fabric_description_index'"
                )
            }
            self.assertIn("display_ui_anchors", fde_columns)
            self.assertNotIn("icon_thumbnail_uri", fde_columns)
            self.assertNotIn("sound_profile_on_movement", fde_columns)
            display_ui_type = connection.execute(
                "SELECT data_type FROM information_schema.columns "
                "WHERE table_name = 'fabric_description_index' "
                "AND column_name = 'display_ui_anchors'"
            ).fetchone()[0]
            self.assertEqual(display_ui_type, "jsonb")
            asset_id = connection.execute(
                "INSERT INTO digital_assets_registry "
                "(sku_identifier, brand_name, rarity_tier, digital_rights_framework) "
                "VALUES (%s, %s, %s, %s::jsonb) RETURNING asset_id",
                (
                    "FGE-DB-TEST-001",
                    "FGE_TEST",
                    "Premium",
                    '{"platform_authorizations":["UNREAL_ENGINE_5"]}',
                ),
            ).fetchone()[0]
            connection.execute(
                "INSERT INTO asset_valuation_event "
                "(asset_id, event_type, currency, gross_value_minor, royalty_bps, platform, license_id) "
                "VALUES (%s, 'LIST', 'USD', 1000, 500, 'UNREAL_ENGINE_5', 'TEST-LICENSE')",
                (asset_id,),
            )
            count = connection.execute(
                "SELECT count(*) FROM asset_valuation_event WHERE asset_id = %s",
                (asset_id,),
            ).fetchone()[0]
            self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
