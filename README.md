# OpenClawMD Skills

**Curated AI Agent Skills for Claude, Gemini, Qwen, Codex & OpenCode**

Collection of 21+ production-ready skills for AI coding agents.

## 📦 Quick Start

### Download Skills

Visit: [openclawmd.com](https://openclawmd.com)

Or download directly from `zips/` folder:

```bash
# Example: Download build:exact
wget https://github.com/DYAI2025/OC-skills/raw/main/zips/build-exact.zip
unzip build-exact.zip -d ~/.agent-deck/skill-db/official/
```

### Install in Agent Deck

```bash
# Download skill
curl -LO https://github.com/DYAI2025/OC-skills/raw/main/zips/build-exact.zip

# Extract to Agent Deck
unzip build-exact.zip -d ~/.agent-deck/skill-db/official/

# Verify installation
~/.agent-deck/skill-db/skill-db.sh list
```

## 📚 Skill Categories

### Core Skills (OpenClawMD Originals)

| Skill | Pattern | Description |
|-------|---------|-------------|
| **build:exact** | Protocol | 3-Phasen Development Framework |
| **consistency-checker** | Python | Auto-check for documentation drift |
| **multi-agent-diagnose** | Protocol | DRA-based diagnosis for skill stacks |

### Superpowers (Claude Originals)

| Skill | Pattern | Description |
|-------|---------|-------------|
| **writing-plans** | Protocol | Create detailed implementation plans |
| **executing-plans** | Protocol | Execute plans in batches |
| **skill-creator** | Protocol | Create new skills |

### Debugging & Diagnostics

| Skill | Pattern | Description |
|-------|---------|-------------|
| **error-diagnostics** | Protocol | Systematic error diagnosis |
| **find-bugs** | Protocol | Automated bug detection |
| **distributed-debugging** | Protocol | Debug distributed systems |

### Code Quality

| Skill | Pattern | Description |
|-------|---------|-------------|
| **codebase-cleanup** | Protocol | Technical debt reduction |
| **dependency-audit** | CLI | Audit project dependencies |
| **fp-ts-errors** | Protocol | FP error handling patterns |

### Architecture & Patterns

| Skill | Pattern | Description |
|-------|---------|-------------|
| **autonomous-agents** | Protocol | AI agent design patterns |
| **react-state** | Protocol | React state management |
| **angular-ui** | Protocol | Angular UI patterns |

### DevOps & Cloud

| Skill | Pattern | Description |
|-------|---------|-------------|
| **azure-functions** | CLI | Deploy Azure Functions |
| **cloudformation** | Protocol | AWS CloudFormation best practices |
| **deployment** | Protocol | Deployment procedures |
| **github-workflows** | Protocol | GitHub Actions automation |

## 🚀 Usage

### Pattern Types

**Protocol** - Workflow/Process skills (no code)
```bash
# Just copy to skills directory
cp protocol-skill.zip ~/.agent-deck/skill-db/official/
unzip protocol-skill.zip
```

**Python Script** - Automation skills
```bash
# Requires Python 3
python3 {{baseDir}}/scripts/script_name.py
```

**CLI Wrapper** - Wrap existing CLI tools
```bash
# Install required binaries first
brew install tool-name
# Then use the skill
```

## 🛠️ Create Your Own Skills

Use our AI-powered generator:

1. Visit [openclawmd.com/generate](https://openclawmd.com/generate)
2. Fill in skill details
3. Download ZIP
4. Install in Agent Deck

## 📊 Statistics

- **Total Skills:** 21
- **Protocols:** 14
- **Python Scripts:** 4
- **CLI Wrappers:** 3
- **Sources:** Antigravity (13), Superpowers (3), SkillKit (1), OpenClawMD (4)

## 🔗 Links

- **Website:** [openclawmd.com](https://openclawmd.com)
- **Agent Deck:** [github.com/asheshgoplani/agent-deck](https://github.com/asheshgoplani/agent-deck)
- **Antigravity:** [github.com/DYAI2025/antigravity-awesome-skills](https://github.com/DYAI2025/antigravity-awesome-skills)

---

**Built with ❤️ by OpenClawMD Team**
