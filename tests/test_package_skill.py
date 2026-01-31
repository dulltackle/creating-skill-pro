
import unittest
import sys
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

# Add scripts directory to path
current_dir = Path(__file__).resolve().parent
scripts_dir = current_dir.parent / 'creating-skill-pro' / 'scripts'
sys.path.append(str(scripts_dir))

from package_skill import package_skill

class TestPackageSkill(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.skill_name = 'testing-skill'
        self.skill_dir = Path(self.test_dir) / self.skill_name
        self.skill_dir.mkdir()
        self.script_dir = Path(self.skill_dir) / 'script'
        self.script_dir.mkdir()

        # Create a valid skill structure
        (self.skill_dir / 'SKILL.md').write_text(f"---\nname: {self.skill_name}\ndescription: A valid description.\n---")
        (self.script_dir / 'script.py').write_text("print('hello')")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_package_skill_success(self):
        # Default output dir (cwd) - careful not to pollute the repo
        # So we pass output_dir
        output_dir = Path(self.test_dir) / 'dist'
        output_dir.mkdir()

        result = package_skill(self.skill_dir, output_dir)

        self.assertIsNotNone(result)
        self.assertTrue(result.exists())
        self.assertEqual(result.name, f"{self.skill_name}.skill")
        self.assertEqual(result.parent, output_dir)

        # Verify zip content
        with zipfile.ZipFile(result, 'r') as z:
            namelist = z.namelist()
            # Paths in zip are relative to the parent directory of the skill
            self.assertIn(f'{self.skill_name}/SKILL.md', namelist)
            self.assertIn(f'{self.skill_name}/script/script.py', namelist)

    def test_package_skill_validation_failure(self):
        # Make skill invalid
        (self.skill_dir / 'SKILL.md').unlink()

        result = package_skill(self.skill_dir, self.test_dir)
        self.assertIsNone(result)

    def test_skill_not_found(self):
        result = package_skill(Path(self.test_dir) / self.skill_name / 'non-existent')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
