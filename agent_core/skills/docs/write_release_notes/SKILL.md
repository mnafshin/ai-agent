# Skill: Write Release Notes

## Metadata
- **MODEL**: GPT-5.4 (`gpt-5.4-2026-02-15`)
- **TEAM**: Documentation
- **ROLE**: Technical Writer / Product Manager

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `OPENAI_KEY` | Direct OpenAI billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Create comprehensive release notes summarizing features, fixes, and deployment information.

## Input
- List of completed tasks
- Code changes (git log or diff)
- Bug fixes from debug log
- Memory files with decisions
- Deployment information

## Process Steps
1. Gather all deliverables from the release
2. Categorize changes (features, fixes, improvements)
3. Write clear summaries for each change
4. Highlight breaking changes if any
5. Include upgrade instructions if needed
6. Document known issues if any
7. Include performance improvements
8. Add links to documentation

## Output Format
```markdown
# Release Notes v1.2.0 - March 7, 2026

## New Features
- **Product Bulk Import**: New API endpoint for importing products from CSV
- **Advanced Search**: Full-text search on product descriptions
- **Audit Logging**: All product modifications are now logged

## Improvements
- 40% faster product search using new indexing strategy
- Reduced API memory footprint by 15%

## Bug Fixes
- Fixed null pointer exception when importing products without category
- Fixed race condition in concurrent product updates
- Fixed SQL injection vulnerability in search filter

## Breaking Changes
- Removed deprecated `/api/v1/products/old-endpoint` - use `/api/v1/products` instead
- Changed authentication from Basic Auth to OAuth2

## Upgrade Instructions
1. Backup the database
2. Run migrations: `./bin/migrate.sh`
3. Restart application
4. Verify health: `curl http://localhost:8080/health`

## Known Issues
- Search performance may be slow on first run (building indexes)
- OAuth migration requires manual configuration

## Contributors
- Alice (Product Management)
- Bob (Architecture)
- Carol (Frontend Development)
- Dave (QA)
```

## Memory Update
**Action**: Append to `memory/release_notes.md`

## Critic Criteria
- ✓ Release notes are clear and comprehensive
- ✓ All major changes documented
- ✓ Breaking changes highlighted
- ✓ Upgrade instructions complete
- ✓ Known issues documented
- ✓ Version follows semantic versioning

## Quality Threshold
80/100 - Release notes help users understand what changed

## Notes
- Be clear about impact (who cares about this change)
- Highlight breaking changes prominently
- Include upgrade instructions
- Document known issues and workarounds
- Thank contributors
- Provide rollback procedures if needed
- Link to more detailed docs
