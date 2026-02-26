#!/usr/bin/env python3
"""
OpenClawMD Skill Converter

Converts skills from Antigravity/Napkin/SkillKit/Superpowers
to OpenClawMD-compatible format.

Usage:
    python3 convert_skills.py [source_dir] [output_dir]
"""

import yaml
import json
import shutil
from pathlib import Path
from datetime import datetime

# Source directories
SOURCES = [
    Path('/tmp/antigravity-awesome-skills/web-app/public/skills'),
    Path('/tmp/napkin'),
    Path('/tmp/skillkit'),
    Path('/tmp/superpowers'),
]

# Output directory
OUTPUT_DIR = Path('/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/CLI_IDE/agent-deck/agent-deck/skills/openclaw-imports')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Curated list of best skills to import
CURATED_SKILLS = [
    # Antigravity - Development
    'error-diagnostics-error-trace',
    'find-bugs',
    'codebase-cleanup-tech-debt',
    'dependency-management-deps-audit',
    'distributed-debugging-debug-trace',
    
    # Antigravity - Cloud/DevOps
    'azure-functions',
    'cloudformation-best-practices',
    'deployment-procedures',
    'github-workflow-automation',
    
    # Antigravity - Architecture
    'autonomous-agent-patterns',
    'angular-ui-patterns',
    'react-state-management',
    'fp-ts-errors',
    
    # Superpowers (the original 3-phase ones)
    'brainstorming-into-designs',
    'writing-plans',
    'executing-plans',
    
    # SkillKit
    'skill-creator',
    'skill-validator',
    'skill-installer',
]


def convert_skill(source_path: Path, skill_name: str) -> dict:
    """Convert a single skill to OpenClawMD format"""
    
    # Read original SKILL.md
    skill_md_path = source_path / 'SKILL.md'
    if not skill_md_path.exists():
        return None
    
    with open(skill_md_path, 'r') as f:
        content = f.read()
    
    # Parse frontmatter
    try:
        frontmatter_end = content.index('---', 3)
        frontmatter_yaml = content[4:frontmatter_end]
        frontmatter = yaml.safe_load(frontmatter_yaml)
        body = content[frontmatter_end+4:].strip()
    except:
        frontmatter = {}
        body = content
    
    # Determine pattern
    if 'scripts/' in content or '.py' in content:
        pattern = 'python-script'
    elif 'bash' in content or 'shell' in content or 'command' in content:
        pattern = 'cli-wrapper'
    else:
        pattern = 'protocol'
    
    # Create OpenClawMD-compatible SKILL.md
    new_frontmatter = {
        'name': skill_name,
        'description': frontmatter.get('description', frontmatter.get('name', skill_name)),
        'compatibility': 'claude, opencode, gemini, codex, qwen',
        'version': frontmatter.get('version', '1.0.0'),
        'author': frontmatter.get('author', 'OpenClawMD (imported)'),
        'pattern': pattern
    }
    
    new_skill_md = f"""---
name: {new_frontmatter['name']}
description: {new_frontmatter['description']}
compatibility: {new_frontmatter['compatibility']}
version: {new_frontmatter['version']}
author: {new_frontmatter['author']}
pattern: {new_frontmatter['pattern']}
---

{body}

---

## OpenClawMD Import

This skill was imported from Antigravity/Superpowers collection.
Converted to OpenClawMD format on {datetime.now().strftime('%Y-%m-%d')}.
"""
    
    return {
        'name': skill_name,
        'description': new_frontmatter['description'],
        'pattern': pattern,
        'content': new_skill_md,
        'original_path': str(source_path)
    }


def main():
    print("🚀 OpenClawMD Skill Converter")
    print("=" * 60)
    
    converted = []
    
    # Process curated skills from Antigravity
    antigravity_path = SOURCES[0]
    print(f"\n📁 Scanning Antigravity: {antigravity_path}")
    
    for skill_name in CURATED_SKILLS:
        skill_path = antigravity_path / skill_name
        if not skill_path.exists():
            # Try to find similar name
            for p in antigravity_path.iterdir():
                if p.is_dir() and skill_name.lower() in p.name.lower():
                    skill_path = p
                    break
        
        if skill_path.exists() and skill_path.is_dir():
            print(f"  Converting: {skill_name}")
            result = convert_skill(skill_path, skill_name)
            if result:
                converted.append(result)
                
                # Save to output directory
                output_skill_dir = OUTPUT_DIR / skill_name
                output_skill_dir.mkdir(parents=True, exist_ok=True)
                
                # Write SKILL.md
                with open(output_skill_dir / 'SKILL.md', 'w') as f:
                    f.write(result['content'])
                
                # Copy references/ if exists
                refs_dir = skill_path / 'references'
                if refs_dir.exists():
                    shutil.copytree(refs_dir, output_skill_dir / 'references', dirs_exist_ok=True)
                
                # Copy scripts/ if exists
                scripts_dir = skill_path / 'scripts'
                if scripts_dir.exists():
                    shutil.copytree(scripts_dir, output_skill_dir / 'scripts', dirs_exist_ok=True)
                
                # Copy assets/ if exists
                assets_dir = skill_path / 'assets'
                if assets_dir.exists():
                    shutil.copytree(assets_dir, output_skill_dir / 'assets', dirs_exist_ok=True)
    
    # Process Superpowers
    superpowers_path = SOURCES[3]
    print(f"\n📁 Scanning Superpowers: {superpowers_path}")
    
    for p in superpowers_path.iterdir():
        if p.is_dir() and (p / 'SKILL.md').exists():
            skill_name = p.name
            if skill_name not in [c['name'] for c in converted]:
                print(f"  Converting: {skill_name}")
                result = convert_skill(p, skill_name)
                if result:
                    converted.append(result)
                    
                    output_skill_dir = OUTPUT_DIR / skill_name
                    output_skill_dir.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_skill_dir / 'SKILL.md', 'w') as f:
                        f.write(result['content'])
    
    print("\n" + "=" * 60)
    print(f"✅ Converted {len(converted)} skills")
    print(f"📂 Output: {OUTPUT_DIR}")
    
    # Generate manifest
    manifest = {
        'generated_at': datetime.now().isoformat(),
        'source_repos': [str(p) for p in SOURCES],
        'skills': [
            {
                'name': s['name'],
                'description': s['description'],
                'pattern': s['pattern'],
                'path': f'skills/openclaw-imports/{s["name"]}'
            }
            for s in converted
        ]
    }
    
    with open(OUTPUT_DIR / 'manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n📋 Manifest saved to: {OUTPUT_DIR / 'manifest.json'}")
    
    # Print summary by pattern
    patterns = {}
    for s in converted:
        patterns[s['pattern']] = patterns.get(s['pattern'], 0) + 1
    
    print("\n📊 Pattern Distribution:")
    for pattern, count in sorted(patterns.items()):
        print(f"  {pattern}: {count}")


if __name__ == '__main__':
    main()
