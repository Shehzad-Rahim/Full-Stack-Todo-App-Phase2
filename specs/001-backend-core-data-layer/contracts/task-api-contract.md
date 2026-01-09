# API Contract: Task Management Service

## Base Path
```
/api/{user_id}
```

## Operations

### Create Task
```
POST /tasks
```

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean (optional, default: false)"
}
```

#### Response
**201 Created**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "string/integer",
  "created_at": "datetime string",
  "updated_at": "datetime string"
}
```

**400 Bad Request**: Invalid input data

### List Tasks
```
GET /tasks
```

#### Response
**200 OK**
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "user_id": "string/integer",
    "created_at": "datetime string",
    "updated_at": "datetime string"
  }
]
```

### Get Task
```
GET /tasks/{id}
```

#### Response
**200 OK**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "string/integer",
  "created_at": "datetime string",
  "updated_at": "datetime string"
}
```

**404 Not Found**: Task does not exist for the given user

### Update Task
```
PUT /tasks/{id}
```

#### Request
**Content-Type**: `application/json`

**Body**:
```json
{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean"
}
```

#### Response
**200 OK**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "string/integer",
  "created_at": "datetime string",
  "updated_at": "datetime string"
}
```

**400 Bad Request**: Invalid input data

**404 Not Found**: Task does not exist for the given user

### Delete Task
```
DELETE /tasks/{id}
```

#### Response
**204 No Content**: Task successfully deleted

**404 Not Found**: Task does not exist for the given user

### Toggle Task Completion
```
PATCH /tasks/{id}/complete
```

#### Response
**200 OK**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "string/integer",
  "created_at": "datetime string",
  "updated_at": "datetime string"
}
```

**404 Not Found**: Task does not exist for the given user

## Security
- All endpoints enforce user isolation by filtering on user_id
- Users can only access tasks that belong to their user_id

## Error Responses
Common error responses across all endpoints:

**400 Bad Request**:
```json
{
  "detail": "Error description"
}
```

**404 Not Found**:
```json
{
  "detail": "Item not found"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```