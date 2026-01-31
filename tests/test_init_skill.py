
import unittest
import sys
import os
import shutil
import tempfile
from pathlib import Path

# Add scripts directory to path
current_dir = Path(__file__).resolve().parent
scripts_dir = current_dir.parent / 'creating-skill-pro' / 'scripts'
sys.path.append(str(scripts_dir))

from init_skill import init_skill, title_case_skill_name

class TestInitSkill(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_title_case(self):
        self.assertEqual(title_case_skill_name('my-skill'), 'My Skill')
        self.assertEqual(title_case_skill_name('testing-something-new'), 'Testing Something New')

    def test_init_skill_success(self):
        skill_name = 'creating-test'
        result = init_skill(skill_name, self.test_dir)

        expected_path = Path(self.test_dir) / skill_name
        self.assertEqual(result, expected_path)
        self.assertTrue(expected_path.exists())
        self.assertTrue(expected_path.is_dir())

        # Check SKILL.md
        skill_md = expected_path / 'SKILL.md'
        self.assertTrue(skill_md.exists())
        content = skill_md.read_text()
        self.assertIn(f"name: {skill_name}", content)
        self.assertIn("# Creating Test", content)

        # Check subdirectories
        self.assertTrue((expected_path / 'scripts').is_dir())
        self.assertTrue((expected_path / 'references').is_dir())
        self.assertTrue((expected_path / 'assets').is_dir())

        # Check example files
        self.assertTrue((expected_path / 'scripts' / 'example.py').exists())
        self.assertTrue((expected_path / 'references' / 'api_reference.md').exists())
        self.assertTrue((expected_path / 'assets' / 'example_asset.txt').exists())

    def test_init_skill_already_exists(self):
        skill_name = 'existing-skill'
        skill_dir = Path(self.test_dir) / skill_name
        skill_dir.mkdir()

        result = init_skill(skill_name, self.test_dir)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
