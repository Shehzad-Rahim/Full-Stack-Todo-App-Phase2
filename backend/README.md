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

All API endpoints enforce user-based data isolation by:
- Filtering queries by user_id parameter
- Returning 404 for tasks that don't belong to the requesting user
- Validating user_id format and existence