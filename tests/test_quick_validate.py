
import unittest
import sys
import os
import shutil
import tempfile
from pathlib import Path

# Add scripts directory to path to allow importing
current_dir = Path(__file__).resolve().parent
scripts_dir = current_dir.parent / 'creating-skill-pro' / 'scripts'
sys.path.append(str(scripts_dir))

from quick_validate import validate_skill

class TestQuickValidate(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.skill_dir = Path(self.test_dir) / 'test-skill'
        self.skill_dir.mkdir()
        self.skill_md = self.skill_dir / 'SKILL.md'

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_skill_md(self, content):
        self.skill_md.write_text(content)

    def test_skill_folder_not_found(self):
        result = validate_skill(Path(self.test_dir) / 'non-existent')
        self.assertIsNone(result)

    def test_path_not_directory(self):
        file_path = Path(self.test_dir) / 'file.txt'
        file_path.touch()
        result = validate_skill(file_path)
        self.assertIsNone(result)

    def test_skill_md_missing(self):
        # Empty directory
        result = validate_skill(self.skill_dir)
        self.assertIsNone(result)

    def test_no_frontmatter(self):
        self.create_skill_md("# Just a title")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertEqual(msg, "No YAML frontmatter found")

    def test_invalid_frontmatter_yaml(self):
        self.create_skill_md("---\nkey: : value\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertIn("Invalid YAML", msg)

    def test_missing_name(self):
        self.create_skill_md("---\ndescription: test\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertEqual(msg, "Missing 'name' in frontmatter")

    def test_missing_description(self):
        self.create_skill_md("---\nname: test-skill\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertEqual(msg, "Missing 'description' in frontmatter")

    def test_disallowed_frontmatter_property(self):
        # 测试 frontmatter 包含了不被允许的属性
        self.create_skill_md("---\nname: testing-skill\ndescription: A valid description.\nextra_field: not allowed\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertIn("Unexpected", msg)

    def test_invalid_name_format(self):
        self.create_skill_md("---\nname: TestSkill\ndescription: test\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertIn("hyphen-case", msg)

    def test_name_too_long(self):
        # 测试 name 值长度超过了64字符
        long_name = "a" * 66
        self.create_skill_md(f"---\nname: {long_name}\ndescription: test\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertIn("too long", msg)

    def test_name_mismatch_directory(self):
        # Directory is 'test-skill', name is 'testing-skill'
        # 'testing-skill' passes gerund check
        self.create_skill_md("---\nname: testing-skill\ndescription: test\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertIn("must match directory name", msg)

    def test_reserved_name(self):
        # Use a name that passes gerund check but contains reserved word
        # 'creating-anthropic'
        reserved_dir = Path(self.test_dir) / 'creating-anthropic'
        reserved_dir.mkdir()
        (reserved_dir / 'SKILL.md').write_text("---\nname: creating-anthropic\ndescription: test\n---")

        valid, msg = validate_skill(reserved_dir)
        self.assertFalse(valid)
        self.assertIn("reserved", msg)

    def test_name_gerund(self):
        # 'test-skill' starts with 'test' which doesn't end in 'ing'
        self.create_skill_md("---\nname: test-skill\ndescription: test\n---")
        valid, msg = validate_skill(self.skill_dir)
        self.assertFalse(valid)
        self.assertIn("gerund form", msg)

    def test_description_too_long(self):
        # 需要一个通过所有 Name 检查的 Skill
        valid_dir = Path(self.test_dir) / 'testing-skill-long-desc'
        valid_dir.mkdir()

        long_description = "a" * 1025
        (valid_dir / 'SKILL.md').write_text(f"---\nname: testing-skill-long-desc\ndescription: {long_description}\n---")

        valid, msg = validate_skill(valid_dir)
        self.assertFalse(valid)
        self.assertIn("Description is too long", msg)

    def test_valid_skill(self):
        # Rename directory to valid gerund name
        valid_dir = Path(self.test_dir) / 'testing-skill'
        valid_dir.mkdir()
        (valid_dir / 'SKILL.md').write_text("---\nname: testing-skill\ndescription: A valid description.\n---")

        valid, msg = validate_skill(valid_dir)
        self.assertTrue(valid)
        self.assertEqual(msg, "Skill is valid!")

if __name__ == '__main__':
    unittest.main()
