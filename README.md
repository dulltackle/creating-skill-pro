# Creating Skill Pro

## Overview

`creating-skill-pro` 是一个用于编写和完善 Codex/Agent Skills 的技能模板与指南，提供技能结构规范、示例参考，以及初始化/校验/打包脚本，帮助你更快产出可复用的高质量 Skill。

## Why This Matters

- **Problem:** 新建 Skill 时常见问题包括结构不统一、`SKILL.md` frontmatter 不规范、描述触发条件不清晰，以及缺少标准化校验与打包流程。
- **Solution:** 该项目提供一套可直接复用的 Skill 指南（`creating-skill-pro/SKILL.md`）、参考文档（`references/`）和脚本工具（`scripts/`），覆盖创建、验证、打包的关键步骤。
- **Value:** 你可以更快创建符合规范的 Skill，减少反复修改与验证成本，并提高 Skill 的可维护性与可分发性。

## Installation

### 1. 克隆仓库

```bash
git clone <your-repo-url> /home/dulltackle/code/creating-skill-pro
cd /home/dulltackle/code/creating-skill-pro
```

### 2. 安装脚本依赖（用于校验/打包）

`quick_validate.py` 使用 `PyYAML`，请确保已安装：

```bash
python3 -m pip install pyyaml
```

### 3. 安装技能到 Agent Skills 目录（按需）

将 `creating-skill-pro/` 目录复制到你的 `$AGENT_HOME/skills`（或当前环境使用的 skills 目录）中，例如：

```bash
cp -R creating-skill-pro "$AGENT_HOME/skills/creating-skill-pro"
```

## Usage Examples

### 示例 1：创建一个新 Skill 骨架

使用初始化脚本创建新技能目录（示例名需符合命名规则，如以 `-ing` 形式开头）：

```bash
python3 creating-skill-pro/scripts/init_skill.py analyzing-spreadsheets --path /tmp/skills
```

预期结果：

- 创建 `/tmp/skills/analyzing-spreadsheets/`
- 生成 `SKILL.md`
- 生成 `scripts/`、`references/`、`assets/` 示例内容

### 示例 2：快速校验 Skill 合规性

```bash
python3 creating-skill-pro/scripts/quick_validate.py /tmp/skills/analyzing-spreadsheets
```

预期结果：

- 成功时显示 `✅ Skill is valid!`
- 失败时显示具体 frontmatter 或命名错误原因

### 示例 3：打包为可分发 `.skill` 文件

```bash
python3 creating-skill-pro/scripts/package_skill.py /tmp/skills/analyzing-spreadsheets ./dist
```

预期结果：

- 自动先执行校验
- 在 `./dist` 下生成 `analyzing-spreadsheets.skill`

## Troubleshooting

### 1. `ModuleNotFoundError: No module named 'yaml'`

- **原因：** 未安装 `PyYAML`
- **解决：** 执行 `python3 -m pip install pyyaml`

### 2. `Validation failed: No YAML frontmatter found`

- **原因：** `SKILL.md` 缺少以 `---` 包裹的 YAML frontmatter
- **解决：** 在 `SKILL.md` 顶部添加合法 frontmatter，并包含 `name` 和 `description`

### 3. `Name 'xxx' should be hyphen-case...`

- **原因：** `name` 不符合小写连字符格式（`kebab-case`）
- **解决：** 使用小写字母/数字/连字符，例如 `analyzing-spreadsheets`

### 4. `Name should use gerund form...`

- **原因：** 技能名第一段未使用 `-ing` 动名词形式（此项目的校验规则）
- **解决：** 将名称改为类似 `creating-*`、`analyzing-*`、`processing-*`

### 5. `Name '...' must match directory name '...' exactly`

- **原因：** `SKILL.md` 中的 `name` 与技能文件夹名不一致
- **解决：** 保持目录名与 frontmatter `name` 完全一致

### 6. 打包失败但校验通过

- **原因：** 输出目录权限或路径问题
- **解决：** 检查输出目录是否可写，或显式指定当前目录下的 `./dist`

## Acknowledgments

This project is inspired by and builds upon the [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) from the [Anthropics Skills](https://github.com/anthropics/skills) repository.
