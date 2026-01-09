---
name: backend-routes-and-db
description: Design and implement backend routes, handle HTTP requests and responses, and connect applications to databases.
---

# Backend Routes & Database Handling

## Instructions

1. **Route design**
   - Define RESTful routes (GET, POST, PUT/PATCH, DELETE)
   - Use clear and consistent URL naming conventions
   - Separate routes by resource or module

2. **Request handling**
   - Validate request parameters and payloads
   - Parse headers, query params, and body data
   - Handle authentication and authorization where required

3. **Response handling**
   - Return proper HTTP status codes
   - Use consistent JSON response structures
   - Handle and format errors gracefully

4. **Database connectivity**
   - Establish secure connections to the database
   - Use environment variables for credentials
   - Implement CRUD operations using ORM or query builders

## Best Practices
- Follow REST or API design standards
- Keep controllers thin and business logic modular
- Sanitize and validate all incoming data
- Use async/await and proper error handling
- Close or reuse database connections efficiently

## Example Structure
```js
// routes/user.routes.js
import express from "express";
import { getUsers, createUser } from "../controllers/user.controller.js";

const router = express.Router();

router.get("/users", getUsers);
router.post("/users", createUser);

export default router;
