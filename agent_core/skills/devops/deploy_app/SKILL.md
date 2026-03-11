# Skill: Deploy App

## Metadata
- **MODEL**: GPT-5.4 (`gpt-5.4-2026-02-15`)
- **TEAM**: DevOps
- **ROLE**: DevOps Engineer

## Auth
| Priority | Key | Notes |
|----------|-----|-------|
| 1 (preferred) | `GITHUB_COPILOT_TOKEN` | Covers all models |
| 2 (override) | `OPENAI_KEY` | Direct OpenAI billing |

Auth resolved by `ModelRouter` in `copilot_models.py`.

## Goal
Create deployment scripts and procedures for deploying application to staging or production environments.

## Input
- Build artifacts
- Deployment target (Docker, Kubernetes, VM, serverless, etc.)
- Deployment configuration (env vars, secrets, resources)
- Memory/decisions on infrastructure
- Health check requirements

## Process Steps
1. Identify deployment target and technology
2. Create deployment script (bash, Python, ansible, etc.)
3. Include pre-deployment checks (health, backups)
4. Define deployment steps (pull, build, start, verify)
5. Include health check procedures
6. Define rollback procedures
7. Create post-deployment verification
8. Document deployment process

## Output Format
```bash
#!/bin/bash
set -e

echo "Starting deployment to production..."

# Pull latest code
git pull origin main

# Build application
mvn clean package -DskipTests

# Create Docker image
docker build -t product-api:latest .
docker push registry.example.com/product-api:latest

# Deploy to Kubernetes
kubectl set image deployment/product-api \\
  product-api=registry.example.com/product-api:latest

# Wait for rollout
kubectl rollout status deployment/product-api

# Health check
curl -f http://product-api/health || exit 1

echo "Deployment successful!"
```

## Memory Update
**Action**: Append to `memory/deployments.md`

## Critic Criteria
- ✓ Deployment script is idempotent (safe to run multiple times)
- ✓ Health checks included
- ✓ Rollback procedure documented
- ✓ Pre-deployment validation included
- ✓ Error handling and logging included
- ✓ Deployment can be automated

## Quality Threshold
85/100 - Deployments must be reliable

## Notes
- Automate everything possible
- Include dry-run mode for testing
- Document manual intervention steps if needed
- Include credentials/secrets management
- Test deployment procedure before using
- Include monitoring and alerting setup
- Plan for quick rollback if issues
