---
id: 1
title: Update Todo App Constitution
stage: constitution
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.constitution
labels: [constitution, todo-app, full-stack, agentic-dev]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
Project: Todo Full-Stack Web Application (Agentic Dev Stack)

Objective:
Transform a basic console-based todo application into a modern, secure, multi-user full-stack web application using a strictly spec-driven, agentic development workflow with no manual coding.

Core principles:
- Spec-driven correctness: All implementation must strictly follow the approved specs
- Security by design: Authentication, authorization, and user isolation are mandatory at every layer
- Determinism: Identical specs must yield reproducible plans and implementations
- Separation of concerns: Frontend, backend, authentication, and data layers must remain clearly decoupled
- Zero manual coding: All code must be generated via Claude Code from specs and plans only

Key standards:
- API correctness: RESTful endpoints must conform exactly to defined methods, paths, and behaviors
- Authentication enforcement: All API routes require valid JWT authentication after auth integration
- User isolation: Users may only access and mutate their own tasks
- Data integrity: Persistent storage must be enforced via Neon Serverless PostgreSQL
- Type safety: Clear data models and schemas must be defined and consistently used
- Error handling: Proper HTTP status codes (200, 201, 400, 401, 403, 404) must be returned
- Environment parity: Frontend and backend must share JWT secrets via environment variables

Architecture constraints:
- Frontend: Next.js 16+ using App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT plugin enabled
- Communication: REST over HTTP with Authorization: Bearer <JWT> headers

Security constraints:
- JWT tokens must be verified on every request
- Tokens must be signed and verified using a shared secret (BETTER_AUTH_SECRET)
- Requests without valid tokens must return 401 Unauthorized
- User ID from JWT must be validated against route parameters
- Task ownership must be enforced at the query level

Development constraints:
- Agentic Dev Stack workflow is mandatory:
  1. Write spec
  2. Generate plan
  3. Break into tasks
  4. Implement via Claude Code
- No handwritten code, patches, or manual edits
- All logic must originate from specs and plans
- Iterations must preserve alignment with the original spec

Quality standards:
- Backend must be stateless and horizontally scalable
- Frontend must be responsive and usable on desktop and mobile
- API responses must be JSON and consistently structured
- Database schema must support multi-user scalability
- Code must be readable, modular, and production-oriented

Success criteria:
- All five basic-level todo features are implemented as a web application
- All API endpoints function correctly and securely
- Authentication is fully enforced using JWTs
- Users can only see and modify their own tasks
- Data persists across sessions and restarts
- Entire system can be deployed with environment-based configuration
- Project passes spec review, security review, and functional review
```

## Response snapshot

Created a comprehensive constitution file for the Todo Full-Stack Web Application project that incorporates all the specified principles, constraints, and workflow requirements. The constitution includes:

1. Six core principles covering spec-driven correctness, security, determinism, separation of concerns, zero manual coding, and user isolation
2. Architecture constraints defining the technology stack and API standards
3. Security constraints focusing on JWT authentication and data access controls
4. Development workflow requirements following the Agentic Dev Stack methodology
5. Error handling standards for consistent API responses
6. Governance section establishing the authority and amendment process for the constitution

## Outcome

- ✅ Impact: Created comprehensive project constitution reflecting all specified requirements
- 🧪 Tests: None required for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Ready to proceed with spec creation for the todo application
- 🧠 Reflection: The constitution establishes clear governance for the agentic development workflow

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec creation for the todo application features