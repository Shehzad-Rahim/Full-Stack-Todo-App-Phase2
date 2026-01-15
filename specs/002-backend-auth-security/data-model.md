# Data Model: Backend Authentication & API Security

## User Entity

### Fields
- **id**: String (Primary Key) - Unique identifier for the user
- **email**: String (Required, Unique) - User's email address, must be valid email format
- **password_hash**: String (Required) - BCrypt hash of user's password
- **created_at**: DateTime (Auto-generated) - Timestamp when user account was created
- **updated_at**: DateTime (Auto-generated/Updated) - Timestamp when user record was last updated

### Relationships
- **tasks**: One-to-Many relationship with Task entity (one user can have many tasks)
  - Foreign key: task.user_id references user.id

### Validation Rules
- Email must be a valid email format (using Pydantic validation)
- Email must be unique across all users
- Email length: 5-255 characters
- Password must be hashed before storing (never store plain text)
- Password hash must be valid BCrypt hash format

## JWT Token Structure

### Payload Claims
- **sub**: String - Subject (user ID)
- **email**: String - User's email address
- **exp**: Integer - Expiration timestamp (Unix epoch)
- **iat**: Integer - Issued at timestamp (Unix epoch)
- **jti**: String - JWT ID for token revocation (optional)

### Token Properties
- Algorithm: HS256 (HMAC with SHA-256)
- Secret: Stored in BETTER_AUTH_SECRET environment variable
- Expiration: Configurable (default 24 hours from issue time)
- Audience: Not specified (can be added if needed for multi-service architecture)

## Authentication Request/Response Models

### Signup Request
- **email**: String (Required) - User's email address
- **password**: String (Required) - Plain text password (min 8 characters)

### Signin Request
- **email**: String (Required) - User's email address
- **password**: String (Required) - Plain text password

### Authentication Response
- **access_token**: String (Required) - JWT token for API access
- **token_type**: String (Required) - Token type (always "bearer")
- **user_id**: String (Required) - User's unique identifier
- **email**: String (Required) - User's email address

## Task Entity Updates

### Additional Validation
- **user_id**: Must match the authenticated user's ID from JWT token
- Query-level filtering: All task queries must be filtered by user_id to enforce data isolation