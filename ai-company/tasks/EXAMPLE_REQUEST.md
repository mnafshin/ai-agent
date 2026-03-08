# Example Task Request

To create a new request, create a folder: `tasks/request_001/`

## Task File Format

Create numbered files with tasks to execute in order:

### 01_gather_requirements.md
```markdown
# Task 1: Gather Requirements

## Goal
Understand the user request in detail.

## Input
User wants to build a product management REST API with the following capabilities:
- Create, read, update, delete products
- Search products by name
- Bulk import from CSV
- Audit logging for all changes

## Success Criteria
All requirements clearly documented in JSON format with success metrics.
```

### 02_write_spec.md
```markdown
# Task 2: Write Specification

## Goal
Create formal specification for the product API.

## Requirements
- RESTful API design
- 5 CRUD operations
- Search capability
- Audit logging
- GDPR compliance

## Success Criteria
Detailed spec with API endpoints, data models, error handling.
```

### 03_analyze_repository.md
```markdown
# Task 3: Analyze Repository

## Goal
Understand existing code structure and conventions.

## Input
Examine the current Spring Boot project structure, tech stack, and coding standards.

## Success Criteria
Documentation of project structure, frameworks, and conventions.
```

### 04_design_system.md
```markdown
# Task 4: Design System Architecture

## Goal
Design architecture for the new product service.

## Requirements
Based on:
- Specification from Task 2
- Existing repository structure from Task 3
- Spring Boot best practices

## Success Criteria
Complete architecture design with component diagram, interfaces, and integration points.
```

### 05_plan_tasks.md
```markdown
# Task 5: Plan Implementation Tasks

## Goal
Break architecture into atomic development tasks.

## Input
- Architecture design from Task 4
- Specification from Task 2

## Success Criteria
- 8-10 ordered implementation tasks
- Each task specifies files to create/modify
- Clear acceptance criteria
```

### 06_implement_entity.md
```markdown
# Task 6: Implement Product Entity

## Goal
Create the Product JPA entity.

## Acceptance Criteria
- Entity has all required fields
- Proper JPA annotations
- Implementations of equals, hashCode, toString
- Validation annotations

## Files to Create
- src/main/java/com/example/entity/Product.java
```

### 07_implement_repository.md
```markdown
# Task 7: Implement ProductRepository

## Goal
Create Spring Data JPA repository.

## Acceptance Criteria
- Custom query methods for search
- Proper pagination support
- Transaction management

## Files to Create
- src/main/java/com/example/repository/ProductRepository.java
```

### 08_implement_service.md
```markdown
# Task 8: Implement ProductService

## Goal
Create business logic layer.

## Acceptance Criteria
- CRUD operations
- Input validation
- Audit logging
- Transaction handling

## Files to Create
- src/main/java/com/example/service/ProductService.java
```

### 09_implement_controller.md
```markdown
# Task 9: Implement ProductController

## Goal
Create REST API endpoints.

## Acceptance Criteria
- All CRUD endpoints
- Proper HTTP status codes
- Error handling
- API documentation

## Files to Create
- src/main/java/com/example/controller/ProductController.java
```

### 10_write_tests.md
```markdown
# Task 10: Write Unit Tests

## Goal
Create comprehensive test coverage.

## Acceptance Criteria
- 80%+ code coverage
- Happy path tests
- Edge case tests
- Error case tests

## Files to Create
- src/test/java/com/example/service/ProductServiceTest.java
- src/test/java/com/example/controller/ProductControllerTest.java
```

---

## How to Use

1. Create a folder: `tasks/request_001/`
2. Create numbered markdown files (01_*.md, 02_*.md, etc.)
3. Run orchestrator: `python orchestrator.py 001`
4. Monitor progress - orchestrator processes tasks sequentially
5. Check memory/ folder for updates and decisions

## Naming Convention
- Prefix with two-digit number (01_, 02_, etc.)
- Names describe what the task accomplishes
- Orchestrator processes in numeric order
