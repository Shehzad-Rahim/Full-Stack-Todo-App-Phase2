---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations. Use for backend and data-driven applications.
---

# Database Schema Design

## Instructions

1. **Schema planning**
   - Identify core entities
   - Define relationships (one-to-one, one-to-many, many-to-many)
   - Normalize data to reduce redundancy

2. **Table creation**
   - Use clear, consistent naming conventions
   - Define primary keys for every table
   - Add foreign keys to enforce relationships
   - Choose appropriate data types

3. **Migrations**
   - Create versioned migration files
   - Support up and down (rollback) operations
   - Keep migrations small and reversible

## Best Practices
- Use snake_case for table and column names
- Always index foreign keys
- Avoid storing derived or duplicate data
- Add timestamps (`created_at`, `updated_at`) by default
- Test migrations in a staging environment before production

## Example Structure
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);
