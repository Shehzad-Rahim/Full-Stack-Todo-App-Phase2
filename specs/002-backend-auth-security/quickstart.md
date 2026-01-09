# Quickstart Guide: Backend Authentication & API Security

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Update `.env` with your configuration:
   - `BETTER_AUTH_SECRET`: Generate a strong secret key (e.g., `openssl rand -hex 32`)
   - `DATABASE_URL`: Your Neon PostgreSQL connection string

4. **Run database migrations**
   ```bash
   # The application will create tables on startup automatically
   ```

## Running the Application

### Development
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage

### Authentication Flow

1. **Sign up a new user**
   ```bash
   curl -X POST http://localhost:8000/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword"}'
   ```

2. **Sign in to get JWT token**
   ```bash
   curl -X POST http://localhost:8000/auth/signin \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword"}'
   ```

3. **Use JWT token for authenticated requests**
   ```bash
   curl -X GET http://localhost:8000/api/user123/tasks \
     -H "Authorization: Bearer <your-jwt-token>"
   ```

### Available Endpoints

#### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/signin` - Authenticate user and return JWT token

#### Protected Task Operations
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task for user
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Testing

### Run all tests
```bash
cd backend
pytest
```

### Run specific test suites
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/
```

### Test with coverage
```bash
pytest --cov=src --cov-report=html
```

## Environment Variables

- `BETTER_AUTH_SECRET` - Secret key for JWT signing (required)
- `DATABASE_URL` - Neon PostgreSQL connection string (required)
- `ENVIRONMENT` - Set to "development", "staging", or "production" (default: "development")
- `LOG_LEVEL` - Log level (default: "info")