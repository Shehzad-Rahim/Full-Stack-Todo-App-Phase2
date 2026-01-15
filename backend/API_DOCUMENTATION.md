# API Documentation: Todo Backend with Authentication

## Overview
This API provides endpoints for managing tasks with JWT-based authentication. Users must authenticate to access their own tasks.

## Authentication
All endpoints except `/auth/signup` and `/auth/signin` require a valid JWT token in the Authorization header.

### Format
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Authentication

#### POST /auth/signup
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user_id": "user_id",
  "email": "user@example.com"
}
```

**Validation:**
- Email must be valid format
- Password must be at least 8 characters
- Email must be unique

#### POST /auth/signin
Authenticate a user and return a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user_id": "user_id",
  "email": "user@example.com"
}
```

**Errors:**
- 401: Invalid email or password

#### POST /auth/refresh
Refresh an existing JWT token.

**Headers:**
```
Authorization: Bearer <existing_jwt_token>
```

**Response (200):**
```json
{
  "access_token": "new_jwt_token",
  "token_type": "bearer"
}
```

### Tasks (User-Specific)

All task endpoints require the user ID in the URL path and a valid JWT token. The user ID in the JWT token must match the user ID in the URL path.

#### GET /api/{user_id}/tasks
Get all tasks for the authenticated user.

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "user_id": "user_id",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

#### POST /api/{user_id}/tasks
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Task description"
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### GET /api/{user_id}/tasks/{id}
Get a specific task for the authenticated user.

**Response (200):**
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 404: Task not found for this user

#### PUT /api/{user_id}/tasks/{id}
Update a specific task for the authenticated user.

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 404: Task not found for this user

#### DELETE /api/{user_id}/tasks/{id}
Delete a specific task for the authenticated user.

**Response (200):**
```json
{
  "message": "Task deleted successfully"
}
```

**Errors:**
- 404: Task not found for this user

#### PATCH /api/{user_id}/tasks/{id}/complete
Toggle the completion status of a specific task for the authenticated user.

**Request Body:**
```json
{
  "completed": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 404: Task not found for this user

## Error Responses

### Authentication Errors
- 401 Unauthorized: Invalid or missing JWT token
- 403 Forbidden: User ID in token doesn't match user ID in URL

### General Errors
- 400 Bad Request: Invalid request parameters
- 404 Not Found: Resource not found
- 500 Internal Server Error: Unexpected server error

## Rate Limits
- `/auth/signup`: 5 requests per minute
- `/auth/signin`: 10 requests per minute
- `/auth/refresh`: 5 requests per minute

## Security
- All sensitive data is protected by JWT authentication
- Users can only access their own tasks
- Passwords are securely hashed using bcrypt
- Rate limiting prevents abuse