---
name: backend
description: Backend development expert for Python (FastAPI) and Node.js (Express). Strictly uses uv for Python dependency management.
---

# Backend Development Skill

This skill provides expert guidance for building robust and scalable backends.

## Frameworks
- **FastAPI**: Preferred for Python (high performance, automatic OpenAPI). Always use `uv` for setup.
- **Express**: Standard for Node.js backends.

## API Design
- **RESTful Principles**: Use correct HTTP methods and status codes.
- **Validation**: Use `Pydantic` (Python) or `Zod` (Node.js) for schema validation.
- **Authentication**: JWT, OAuth2, and session-based auth.

## Database Management
- **SQL (PostgreSQL)**: Use SQLAlchemy (Python) or Prisma (Node.js).
- **Migrations**: Always use migration tools like `alembic` or `prisma migrate`.

## Scalability
- **Caching**: Redis for session and data caching.
- **Background Tasks**: Celery (Python) or BullMQ (Node.js) for asynchronous processing.
