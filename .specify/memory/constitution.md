<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles: All principles were created/updated
Added sections: Core Principles (6), Architecture Constraints, Security Constraints, Development Workflow
Removed sections: None
Templates requiring updates: ✅ Updated all templates based on new principles
Follow-up TODOs: None
-->
# Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Correctness
All implementation must strictly follow the approved specs. Features and functionality must be derived from documented specifications rather than ad-hoc development decisions.

### Security by Design
Authentication, authorization, and user isolation are mandatory at every layer. No feature may bypass security requirements, and all access controls must be enforced consistently.

### Deterministic Implementation
Identical specs must yield reproducible plans and implementations. The development process must be repeatable and consistent across different developers and environments.

### Separation of Concerns
Frontend, backend, authentication, and data layers must remain clearly decoupled. Cross-layer dependencies must be well-defined interfaces with clear contracts.

### Zero Manual Coding
All code must be generated via Claude Code from specs and plans only. Handwritten code, patches, or manual edits are prohibited unless explicitly approved through the exception process.

### User Isolation Enforcement
Users may only access and mutate their own data. All API endpoints must enforce proper user authorization and data ownership at the query level.

## Architecture Constraints

- **Frontend**: Next.js 16+ using App Router
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT plugin enabled
- **Communication**: REST over HTTP with Authorization: Bearer <JWT> headers
- **API Conformance**: RESTful endpoints must conform exactly to defined methods, paths, and behaviors
- **Type Safety**: Clear data models and schemas must be defined and consistently used

## Security Constraints

- **JWT Token Verification**: JWT tokens must be verified on every authenticated request
- **Token Signing**: Tokens must be signed and verified using a shared secret (BETTER_AUTH_SECRET)
- **Unauthorized Access**: Requests without valid tokens must return 401 Unauthorized
- **User ID Validation**: User ID from JWT must be validated against route parameters
- **Task Ownership**: Task ownership must be enforced at the query level to prevent unauthorized access
- **Environment Parity**: Frontend and backend must share JWT secrets via environment variables

## Development Workflow

- **Agentic Dev Stack Mandatory**: The four-phase workflow must be followed:
  1. Write spec
  2. Generate plan
  3. Break into tasks
  4. Implement via Claude Code
- **Quality Standards**: Backend must be stateless and horizontally scalable
- **Frontend Requirements**: Must be responsive and usable on desktop and mobile
- **API Standards**: Responses must be JSON and consistently structured
- **Database Scalability**: Schema must support multi-user scalability
- **Code Quality**: Must be readable, modular, and production-oriented

## Error Handling Standards

- **HTTP Status Codes**: Proper HTTP status codes (200, 201, 400, 401, 403, 404) must be returned consistently
- **Data Integrity**: Persistent storage must be enforced via Neon Serverless PostgreSQL
- **Validation**: Input validation must occur at both frontend and backend layers

## Governance

This constitution supersedes all other development practices and guidelines. All development activities must comply with these principles. Amendments to this constitution require formal documentation, team approval, and a migration plan for existing code. All pull requests and code reviews must verify compliance with these principles. Exception requests must follow the formal approval process documented in the project governance procedures.

**Version**: 1.1.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
