# Todo Backend Service

Backend service for the Todo Full-Stack Web Application. This service provides RESTful APIs for managing tasks with strict user-based data isolation.

## Features

- RESTful API endpoints for task management
- User-based data isolation (users can only access their own tasks)
- Task CRUD operations (Create, Read, Update, Delete)
- Task completion status toggle
- Neon Serverless PostgreSQL integration
- Comprehensive error handling and validation
- Request/response logging
- Full test coverage (unit and integration tests)

## API Endpoints

### Task Management

- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks` - List all tasks for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task for a user
- `PUT /api/{user_id}/tasks/{id}` - Update a task for a user
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task for a user
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Setup

### Prerequisites

- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:

```bash
# Using pip
pip install -r requirements.txt

# Or using poetry
poetry install
```

### Environment Configuration

Create a `.env` file with the following variables:

```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
ENVIRONMENT="development"
LOG_LEVEL="info"
```

## Running the Application

### Development

```bash
# Using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Using poetry
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Using uvicorn with production settings
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

### Run All Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

## Architecture

The backend follows a clean architecture with the following structure:

```
backend/
├── src/
│   ├── models/          # SQLModel definitions
│   ├── database/        # Database connection and engine
│   ├── api/             # API routes and dependencies
│   │   └── routes/      # Individual route files
│   ├── middleware.py    # Request logging middleware
│   ├── exceptions.py    # Custom exception classes
│   ├── main.py          # FastAPI app instance
│   └── config.py        # Configuration settings
├── tests/               # Test files
│   ├── conftest.py      # Pytest configuration
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Project metadata and settings
```

## Data Model

The Task entity includes the following fields:
- `id`: Integer, Primary Key, Auto-increment
- `title`: String, Required (1-255 characters)
- `description`: String, Optional (up to 1000 characters)
- `completed`: Boolean, Default: False
- `user_id`: String, Required, Indexed for performance
- `created_at`: DateTime, Auto-populated on creation
- `updated_at`: DateTime, Auto-updated on modifications

## Security

### Authentication
The backend service now includes JWT-based authentication for secure API access:

- **JWT Token Authentication**: All endpoints require a valid JWT token in the Authorization header
- **Format**: `Authorization: Bearer <jwt_token>`
- **Token Generation**: Tokens are issued during signup/signin via `/auth/signup` and `/auth/signin` endpoints
- **User Verification**: Token user ID is validated against URL parameter to prevent cross-user access

### Endpoints
- `POST /auth/signup` - Create a new user account
- `POST /auth/signin` - Authenticate user and return JWT token
- `POST /auth/refresh` - Refresh an existing JWT token
- All existing task endpoints now require authentication

### Data Isolation
All API endpoints enforce user-based data isolation by:
- Requiring valid JWT token for access
- Validating that the user ID in the token matches the user ID in the URL parameter
- Returning 403 Forbidden for mismatched user IDs
- Filtering queries by user_id parameter
- Returning 404 for tasks that don't belong to the requesting user
- Validating user_id format and existence

### Rate Limiting
Authentication endpoints are rate-limited:
- `/auth/signup`: 5 requests per minute
- `/auth/signin`: 10 requests per minute
- `/auth/refresh`: 5 requests per minute

### Environment Configuration
Additional environment variables for authentication:
```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
ENVIRONMENT="development"
LOG_LEVEL="info"
BETTER_AUTH_SECRET="your-super-secret-key-change-in-production"
```