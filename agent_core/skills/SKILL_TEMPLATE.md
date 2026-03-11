# Skill Template

## Metadata
- **SKILL_ID**: unique_skill_id
- **TEAM**: Product / Architecture / Development / QA / DevOps / Docs / Control
- **ROLE**: Brief role description
- **MODEL**: model-name (`model-id`)

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `ANTHROPIC_KEY` or `OPENAI_KEY` | Direct billing per provider |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Available Models

### Claude (Reasoning, Review) — Claude 4 Generation
```
claude-4-haiku-20260115      # Haiku 4 – fastest, cheapest (Jan 2026)
claude-4-sonnet-20260201     # Sonnet 4 – balanced (Feb 2026)
claude-4.6-opus-20260301     # Opus 4.6 – most capable (Mar 2026)
```

### GPT (Generation, Testing, Documentation) — GPT-5 Generation
```
gpt-5.4-2026-02-15           # GPT-5.4 – latest, most capable (Feb 2026)
gpt-4-turbo                  # GPT-4 Turbo – legacy
```

## Goal
[Single-sentence goal describing what this skill accomplishes]

## Input
- [Input type 1]
- [Input type 2]
- [Input type 3]

## Process Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

## Output Format
```
[Example output structure]
```

## Memory Update
Which memory files to update and how:
- **decisions.md**: [if applicable]
- **architecture.md**: [if applicable]
- **debug_log.md**: [if applicable]

## Critic Criteria (if applicable)
Quality evaluation criteria (for skills that use critic loop):
- Criterion 1 (weight: X%)
- Criterion 2 (weight: X%)
- Criterion 3 (weight: X%)

**Threshold**: 90/100 to pass

## Notes
Additional guidance or context:
- [Note 1]
- [Note 2]
