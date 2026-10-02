import tomllib
import unittest
from pathlib import Path


class ManifestTests(unittest.TestCase):
    def test_extension_manifest_declares_required_metadata(self) -> None:
        manifest_path = (
            Path(__file__).parents[1]
            / "blender_jev_review"
            / "blender_manifest.toml"
        )
        manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(manifest["schema_version"], "1.0.0")
        self.assertEqual(manifest["id"], "blender_jev_review")
        self.assertEqual(manifest["type"], "add-on")
        self.assertEqual(manifest["license"], ["SPDX:MIT"])
        self.assertIn("network", manifest["permissions"])
        self.assertIn("blender_manifest.toml", manifest["build"]["paths"])


if __name__ == "__main__":
    unittest.main()
