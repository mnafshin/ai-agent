# Skill: Update Docs

## Metadata
- **MODEL**: GPT-5.4 (`gpt-5.4-2026-02-15`)
- **TEAM**: Documentation
- **ROLE**: Technical Writer / Developer Advocate

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `OPENAI_KEY` | Direct OpenAI billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Update technical documentation to reflect new features, APIs, and implementation details.

## Input
- Implementation details and code
- Task description
- Specification from WriteSpec
- Existing documentation structure
- Code comments and docstrings

## Process Steps
1. Identify documentation to update (README, API docs, guides, etc.)
2. Extract relevant details from code
3. Write clear explanations for developers
4. Include code examples
5. Update table of contents
6. Add links between related docs
7. Include troubleshooting section if applicable
8. Verify documentation is accurate

## Output Format
```markdown
# Product Service API

## Overview
The Product Service provides REST API endpoints for managing products in the inventory system.

## Endpoints

### Create Product
**POST** `/api/v1/products`

Request:
```json
{
  "name": "Widget",
  "price": 9.99,
  "description": "A useful widget"
}
```

Response:
```json
{
  "id": 1,
  "name": "Widget",
  "price": 9.99,
  "createdAt": "2026-03-07T10:00:00Z"
}
```

## Error Handling
- 400 Bad Request: Invalid input
- 409 Conflict: Product name already exists
- 500 Internal Error: Server error

## Usage Examples
[code examples]
```

## Memory Update
**Action**: Append to `memory/docs.md`

## Critic Criteria
- ✓ Documentation is clear and concise
- ✓ Code examples are accurate and runnable
- ✓ API documentation includes examples
- ✓ Error cases documented
- ✓ Consistent with existing docs style
- ✓ Includes all new features

## Quality Threshold
80/100 - Documentation helps users understand the system

## Notes
- Write for developers, not non-technical audience
- Include practical examples
- Document both happy path and error cases
- Keep docs in sync with code
- Link to related documentation
- Use consistent formatting and style
- Include troubleshooting section
