# Quickstart: Backend Core & Data Layer

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance
- Environment variables configured for database connection

## Setup

### 1. Clone and Navigate
```bash
# Navigate to project directory
cd /path/to/project
```

### 2. Install Dependencies
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file with the following variables:
```env
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
```

### 4. Database Setup
```bash
# Run database migrations (if using alembic)
poetry run alembic upgrade head

# Or create tables directly
poetry run python -c "from backend.src.database.engine import create_db_and_tables; create_db_and_tables()"
```

## Running the Application

### Development
```bash
# Using Uvicorn directly
uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000

# Using Poetry
poetry run uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Using Uvicorn with production settings
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Task Management
```bash
# Get all tasks for a user
GET /api/{user_id}/tasks

# Create a new task
POST /api/{user_id}/tasks
Content-Type: application/json
{
  "title": "New task",
  "description": "Task description"
}

# Get a specific task
GET /api/{user_id}/tasks/{task_id}

# Update a task
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": false
}

# Delete a task
DELETE /api/{user_id}/tasks/{task_id}

# Toggle task completion
PATCH /api/{user_id}/tasks/{task_id}/complete
```

## Testing

### Run Unit Tests
```bash
# All tests
poetry run pytest

# Unit tests only
poetry run pytest tests/unit/

# Integration tests only
poetry run pytest tests/integration/
```

### Run with Coverage
```bash
poetry run pytest --cov=backend.src --cov-report=html
```

## Configuration

The application uses the following structure:

```
backend/
├── src/
│   ├── models/          # SQLModel definitions
│   ├── database/        # Database connection and engine
│   ├── api/             # API routes and dependencies
│   │   └── routes/      # Individual route files
│   ├── main.py          # FastAPI app instance
│   └── config.py        # Configuration settings
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Project metadata and settings
```

## Environment Variables

- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `ENVIRONMENT`: Set to "development", "staging", or "production"
- `LOG_LEVEL`: Logging level (default: INFO)