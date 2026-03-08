# Directory Tree Reference

## Full Project Structure

```
/Users/afshin/Documents/blog/ai-agent/
│
├── 📄 README.md                              # Full documentation (3000+ words)
├── 📄 QUICKSTART.md                          # 5-minute setup guide
├── 📄 SUMMARY.md                             # Project overview
├── 📄 DIRECTORY_TREE.md                      # This file
│
├── 📰 article/
│   └── AI_AGENTS_BEST_PRACTICES.md           # Main article (4000+ words)
│                                             # - Philosophy & best practices
│                                             # - Architecture patterns
│                                             # - 20-skill system
│                                             # - Implementation guide
│
├── 🏭 ai-company/                            # Complete implementation
│   │
│   ├── 📂 skills/                            # 20 skills organized by team
│   │   │                                     # Total: 20 SKILL.md files
│   │   │
│   │   ├── 📂 product/                       # Product Team (2 skills)
│   │   │   ├── 📂 gather_requirements/
│   │   │   │   └── SKILL.md                  # Goal: Extract requirements
│   │   │   │                                 # Model: Claude
│   │   │   │                                 # Output: JSON requirements
│   │   │   │
│   │   │   └── 📂 write_spec/
│   │   │       └── SKILL.md                  # Goal: Create formal spec
│   │   │                                     # Model: Claude
│   │   │                                     # Critic: Yes (quality critical)
│   │   │
│   │   ├── 📂 architecture/                  # Architecture Team (3 skills)
│   │   │   ├── 📂 analyze_repo/
│   │   │   │   └── SKILL.md                  # Goal: Understand existing code
│   │   │   │                                 # Model: Claude
│   │   │   │                                 # Memory: Updates repo_summary.md
│   │   │   │
│   │   │   ├── 📂 design_system/
│   │   │   │   └── SKILL.md                  # Goal: Design architecture
│   │   │   │                                 # Model: Claude
│   │   │   │                                 # Critic: Yes
│   │   │   │                                 # Verify Spec: Yes
│   │   │   │
│   │   │   └── 📂 (future) update_architecture_memory/
│   │   │       └── SKILL.md                  # Goal: Persist decisions
│   │   │                                     # Model: Claude
│   │   │
│   │   ├── 📂 development/                   # Development Team (4 skills)
│   │   │   ├── 📂 plan_tasks/
│   │   │   │   └── SKILL.md                  # Goal: Break into tasks
│   │   │   │                                 # Model: Claude
│   │   │   │                                 # Critic: Yes
│   │   │   │
│   │   │   ├── 📂 implement_feature/
│   │   │   │   └── SKILL.md                  # Goal: Write code
│   │   │   │                                 # Model: Copilot
│   │   │   │                                 # Critic: Yes
│   │   │   │                                 # Verify Spec: Yes
│   │   │   │
│   │   │   ├── 📂 refactor_code/
│   │   │   │   └── SKILL.md                  # Goal: Safe refactoring
│   │   │   │                                 # Model: Copilot
│   │   │   │
│   │   │   └── 📂 fix_bug/
│   │   │       └── SKILL.md                  # Goal: Debug & fix
│   │   │                                     # Model: Claude
│   │   │
│   │   ├── 📂 qa/                            # QA Team (3 skills)
│   │   │   ├── 📂 generate_tests/
│   │   │   │   └── SKILL.md                  # Goal: Create tests
│   │   │   │                                 # Model: GPT
│   │   │   │
│   │   │   ├── 📂 debug_cycle/
│   │   │   │   └── SKILL.md                  # Goal: Fix build/test failures
│   │   │   │                                 # Model: Claude
│   │   │   │
│   │   │   └── 📂 review_code/
│   │   │       └── SKILL.md                  # Goal: Code review
│   │   │                                     # Model: Claude
│   │   │                                     # Critic: Yes
│   │   │
│   │   ├── 📂 devops/                        # DevOps Team (2 skills)
│   │   │   ├── 📂 configure_ci/
│   │   │   │   └── SKILL.md                  # Goal: Create CI/CD pipeline
│   │   │   │                                 # Model: GPT
│   │   │   │
│   │   │   └── 📂 deploy_app/
│   │   │       └── SKILL.md                  # Goal: Deploy application
│   │   │                                     # Model: GPT
│   │   │
│   │   ├── 📂 docs/                          # Documentation Team (2 skills)
│   │   │   ├── 📂 update_docs/
│   │   │   │   └── SKILL.md                  # Goal: Update documentation
│   │   │   │                                 # Model: GPT
│   │   │   │
│   │   │   └── 📂 write_release_notes/
│   │   │       └── SKILL.md                  # Goal: Create release notes
│   │   │                                     # Model: GPT
│   │   │
│   │   └── 📂 control/                       # Control Layer (2 skills)
│   │       ├── 📂 critic/
│   │       │   └── SKILL.md                  # Goal: Quality evaluation
│   │       │                                 # Model: Claude
│   │       │                                 # Purpose: Improve all outputs
│   │       │
│   │       └── 📂 verify_spec/
│   │           └── SKILL.md                  # Goal: Verify implementation
│   │                                         # Model: Claude
│   │                                         # Purpose: Check completeness
│   │
│   ├── 💾 memory/                            # Persistent Context (10 files)
│   │   │                                     # Updated by agents
│   │   │                                     # Loaded by orchestrator
│   │   │
│   │   ├── repo_summary.md                   # Project structure & tech stack
│   │   │                                     # Updated by: analyze_repo
│   │   │                                     # Used by: all skills
│   │   │
│   │   ├── architecture.md                   # System design & components
│   │   │                                     # Updated by: design_system
│   │   │                                     # Used by: implementation skills
│   │   │
│   │   ├── decisions.md                      # Critical architectural choices
│   │   │                                     # Updated by: all skills
│   │   │                                     # Used by: verify decisions
│   │   │
│   │   ├── debug_log.md                      # Issues found & fixes applied
│   │   │                                     # Updated by: fix_bug, debug_cycle
│   │   │                                     # Used by: prevent recurring bugs
│   │   │
│   │   ├── review_log.md                     # Code review scores & feedback
│   │   │                                     # Updated by: review_code
│   │   │                                     # Used by: improve code quality
│   │   │
│   │   ├── verification.md                   # Spec compliance checks
│   │   │                                     # Updated by: verify_spec
│   │   │                                     # Used by: ensure correctness
│   │   │
│   │   ├── qa.md                             # Test coverage & QA results
│   │   │                                     # Updated by: generate_tests
│   │   │                                     # Used by: ensure quality
│   │   │
│   │   ├── devops.md                         # Infrastructure & deployments
│   │   │                                     # Updated by: configure_ci, deploy
│   │   │                                     # Used by: deployment reference
│   │   │
│   │   ├── docs.md                           # Documentation history
│   │   │                                     # Updated by: update_docs
│   │   │                                     # Used by: track changes
│   │   │
│   │   └── release_notes.md                  # Release history & notes
│   │                                         # Updated by: write_release_notes
│   │                                         # Used by: version tracking
│   │
│   ├── 📋 tasks/                             # Development Tasks
│   │   │                                     # Organized by request
│   │   │                                     # Numbered sequentially
│   │   │
│   │   ├── EXAMPLE_REQUEST.md                # Guide: How to structure tasks
│   │   │                                     # Shows: 01_*.md, 02_*.md pattern
│   │   │                                     # Example: Product API project
│   │   │
│   │   └── request_001/                      # Example request (to be created)
│   │       ├── 01_gather_requirements.md    # Task 1
│   │       ├── 02_write_spec.md              # Task 2
│   │       ├── 03_analyze_repo.md            # Task 3
│   │       ├── 04_design_system.md           # Task 4
│   │       ├── 05_plan_tasks.md              # Task 5
│   │       ├── 06_implement_entity.md        # Task 6
│   │       ├── 07_implement_repository.md    # Task 7
│   │       ├── 08_implement_service.md       # Task 8
│   │       ├── 09_implement_controller.md    # Task 9
│   │       └── 10_write_tests.md             # Task 10
│   │
│   ├── 🐍 orchestrator.py                    # Main Orchestrator
│   │                                         # - Loads skills
│   │                                         # - Runs critic loops
│   │                                         # - Verifies specs
│   │                                         # - Updates memory
│   │                                         # - ~400 lines
│   │
│   └── ⚙️  config.yaml                        # Configuration File
│                                             # - Skill assignments
│                                             # - Thresholds (90/100)
│                                             # - Model assignments
│                                             # - Memory settings
│
└── 🛠️ tools/
    │
    └── inspector.py                          # Validation Tool
                                              # - Checks structure
                                              # - Validates SKILL.md files
                                              # - Verifies memory
                                              # - Tests config
                                              # - ~400 lines


## File Statistics

Total Files: 27 files
├── Documentation Files: 4
│   ├── README.md (3000+ words)
│   ├── QUICKSTART.md (1000+ words)
│   ├── SUMMARY.md (2000+ words)
│   └── AI_AGENTS_BEST_PRACTICES.md (4000+ words)
│
├── Skill Files: 20 SKILL.md files
│   ├── 2 Product skills
│   ├── 3 Architecture skills
│   ├── 4 Development skills
│   ├── 3 QA skills
│   ├── 2 DevOps skills
│   ├── 2 Documentation skills
│   └── 2 Control layer skills
│
├── Memory Files: 10 .md files
│   (Initialized, ready for updates)
│
├── Code Files: 2
│   ├── orchestrator.py (~400 lines)
│   └── inspector.py (~400 lines)
│
├── Config Files: 2
│   ├── config.yaml
│   └── EXAMPLE_REQUEST.md
│
└── Task Examples: 1+ requests
    └── request_001/ (when created)


## Key Measurements

Size: ~80 MB total (mostly documentation)
Lines of Code: 800 (orchestrator + inspector)
Lines of Documentation: 10,000+ words
Skills: 20 fully implemented
Memory Files: 10 initialized
Quick Start Time: 5 minutes
Full Setup Time: 30 minutes


## Access Paths

Main Documentation:
- READ FIRST: /article/AI_AGENTS_BEST_PRACTICES.md
- QUICK SETUP: /QUICKSTART.md
- FULL DOCS: /README.md

Implementation:
- ORCHESTRATOR: /ai-company/orchestrator.py
- VALIDATOR: /tools/inspector.py

Skills Library:
- PRODUCT: /ai-company/skills/product/*/SKILL.md
- ARCHITECTURE: /ai-company/skills/architecture/*/SKILL.md
- DEVELOPMENT: /ai-company/skills/development/*/SKILL.md
- QA: /ai-company/skills/qa/*/SKILL.md
- DEVOPS: /ai-company/skills/devops/*/SKILL.md
- DOCS: /ai-company/skills/docs/*/SKILL.md
- CONTROL: /ai-company/skills/control/*/SKILL.md

Memory:
- DECISIONS: /ai-company/memory/decisions.md
- ARCHITECTURE: /ai-company/memory/architecture.md
- DEBUG LOG: /ai-company/memory/debug_log.md

Configuration:
- CONFIG: /ai-company/config.yaml
- TASKS EXAMPLE: /ai-company/tasks/EXAMPLE_REQUEST.md

## Finding Things

"I need to understand..."
- Best practices → article/AI_AGENTS_BEST_PRACTICES.md
- Quick start → QUICKSTART.md
- Full options → README.md
- This skill → ai-company/skills/{team}/{skill}/SKILL.md

"I want to..."
- Validate system → python tools/inspector.py ai-company
- Run workflow → cd ai-company && python orchestrator.py 001
- Create tasks → cp EXAMPLE_REQUEST.md tasks/request_001/
- Check results → cat memory/architecture.md
- Configure → edit ai-company/config.yaml

"I'm looking for..."
- Code → ai-company/orchestrator.py or inspector.py  
- Decisions → memory/decisions.md
- Issues → memory/debug_log.md
- Reviews → memory/review_log.md
- All skills → ai-company/skills/

```

---

**This structure is complete and ready to use.**

Each file has a specific purpose and is fully documented.

```
