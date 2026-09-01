# School Website Backend

A production-quality FastAPI backend for a school website built with SQLAlchemy 2.0, PostgreSQL, and Alembic.

## Features

- **FastAPI** modern Python web framework with automatic API documentation
- **SQLAlchemy 2.0** typed ORM with async-ready design
- **PostgreSQL** reliable relational database
- **Alembic** for database migrations
- **Pydantic** for request/response validation
- **CORS** middleware for frontend integration
- **Comprehensive tests** with pytest
- **Docker** support for containerized deployment
- **Production-ready** configuration and error handling

## Tech Stack

- Python 3.11+
- FastAPI 0.111+
- SQLAlchemy 2.0+
- PostgreSQL 12+
- Alembic 1.13+
- pytest for testing
- Uvicorn for ASGI server

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   └── configuration/
│   │       └── settings.py          # Application settings
│   ├── database/
│   │   ├── base.py                  # SQLAlchemy base class
│   │   ├── session.py               # Database engine and session
│   │   └── dependencies.py          # FastAPI dependency injection
│   ├── models/
│   │   └── school.py                # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── health.py                # Health check response schema
│   │   └── school.py                # School request/response schemas
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── school.py                # Database query functions
│   ├── routers/
│   │   ├── health.py                # Health check endpoints
│   │   └── school.py                # School CRUD endpoints
│   ├── tests/
│   │   ├── conftest.py              # Pytest fixtures and configuration
│   │   ├── test_health.py           # Health endpoint tests
│   │   └── test_school.py           # School endpoint tests
│   └── main.py                      # FastAPI application entry point
├── alembic/
│   ├── versions/                    # Migration files
│   ├── env.py                       # Alembic environment
│   └── script.py.mako               # Migration template
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Production Docker image
├── docker-compose.yml               # Local development Docker Compose
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

## Local Development Setup

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher
- pip and venv (included with Python)

### 1. Clone the repository

```bash
cd backend
```

### 2. Create and activate virtual environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and update with your local PostgreSQL credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/school_db
SECRET_KEY=your-secure-random-key
APP_ENV=development
DEBUG=true
```

### 5. Create database (if needed)

```bash
createdb school_db  # On Linux/macOS with PostgreSQL installed
```

Or use your PostgreSQL client of choice.

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 8. Access API documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

```
GET /api/health
```

Returns application and database health status.

**Response:**
```json
{
  "status": "ok",
  "app": "School Website",
  "database": "ok"
}
```

### School Endpoints

**Get School**
```
GET /api/school
```

Retrieve school information.

**Create School**
```
POST /api/school
Content-Type: application/json

{
  "name": "School Name",
  "description": "Optional description",
  "address": "123 Main St",
  "phone": "+1-555-0123",
  "email": "info@school.com",
  "logo_url": "https://example.com/logo.png",
  "established_year": 2000
}
```

Returns 201 Created on success, 409 Conflict if a school already exists.

**Update School**
```
PUT /api/school
Content-Type: application/json

{
  "name": "Updated Name",
  "phone": "+1-555-9876"
}
```

All fields are optional for partial updates.

**Delete School**
```
DELETE /api/school
```

Returns 204 No Content on success.

## Running Tests

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=app --cov-report=html
```

Coverage report will be in `htmlcov/index.html`

### Run specific test file

```bash
pytest app/tests/test_school.py -v
```

### Run specific test

```bash
pytest app/tests/test_school.py::TestCreateSchool::test_create_school_success -v
```

## Database Migrations

### Create a new migration

After modifying models:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Review the generated migration file in `alembic/versions/` before applying.

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migrations

```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all migrations
```

### Check migration history

```bash
alembic history
```

## Docker Development

### Build and run with Docker Compose

```bash
docker-compose up -d
```

This will:
1. Start PostgreSQL on port 5432
2. Build the FastAPI application
3. Run Alembic migrations automatically
4. Start the API server on port 8000

### Access the application

- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

### Stop the services

```bash
docker-compose down
```

To also remove volumes:
```bash
docker-compose down -v
```

## Production Deployment

### Prepare for deployment

1. **Set secure environment variables:**
   - `SECRET_KEY` - Generate a strong random key
   - `DATABASE_URL` - Use your production database
   - `APP_ENV` - Set to "production"
   - `DEBUG` - Set to "false"
   - `CORS_ORIGINS` - Set to your frontend domain(s)

2. **Never commit secrets:**
   - `.env` is ignored by git
   - Use deployment platform's environment variable management
   - Rotate `SECRET_KEY` regularly

3. **Database setup:**
   - Ensure PostgreSQL is running and accessible
   - Create an empty database for the application
   - The application will run migrations on startup

### Deploy with Docker

1. **Build the image:**
   ```bash
   docker build -t school-backend:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     -e DATABASE_URL="postgresql://user:password@host:5432/school_db" \
     -e SECRET_KEY="your-secure-key" \
     -e APP_ENV="production" \
     -e DEBUG="false" \
     -e CORS_ORIGINS="https://your-frontend.com" \
     -p 8000:8000 \
     school-backend:latest
   ```

### Deploy to cloud platforms

The backend can be deployed to any platform supporting Python/Docker:

**Render.com:**
- Connect GitHub repository
- Set Environment Variables in dashboard
- Add build command: `pip install -r requirements.txt && alembic upgrade head`
- Add start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**Railway.app:**
- Connect GitHub repository
- Set environment variables
- Add variables.yml or set in dashboard
- Application auto-detects Dockerfile

**Heroku:**
- Create Procfile: `web: alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Set config vars in dashboard
- Deploy with `git push heroku main`

**AWS EC2:**
- Install Python 3.11, PostgreSQL client
- Clone repository
- Set up virtual environment and install dependencies
- Configure environment variables
- Run migrations: `alembic upgrade head`
- Use Gunicorn for production:
  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
  ```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | School Website | Application name |
| `APP_ENV` | development | Environment (development/production) |
| `DEBUG` | true | Enable debug mode |
| `DATABASE_URL` | postgresql://localhost:5432/school_db | PostgreSQL connection URL |
| `SECRET_KEY` | change-me-in-production | Secret key for security |
| `CORS_ORIGINS` | http://localhost:3000,http://localhost:5173 | Comma-separated CORS origins |
| `ALLOWED_HOSTS` | localhost,127.0.0.1 | Allowed host names |

### Database Connection String Format

```
postgresql://username:password@host:port/database_name
```

**Examples:**
- Local: `postgresql://postgres:postgres@localhost:5432/school_db`
- Docker Compose: `postgresql://postgres:postgres@db:5432/school_db`
- Remote: `postgresql://user:pass@db.example.com:5432/school_db`

## Troubleshooting

### Database connection refused

**Error:** `Could not connect to server: Connection refused`

**Solution:**
1. Verify PostgreSQL is running
2. Check `DATABASE_URL` in `.env`
3. Verify credentials and permissions
4. For Docker, ensure PostgreSQL container is healthy: `docker-compose ps`

### Alembic migrations not applied

**Error:** `(psycopg2.errors.UndefinedTable) relation "schools" does not exist`

**Solution:**
```bash
alembic upgrade head
```

### Port already in use

**Error:** `Address already in use` for port 8000

**Solution:**
```bash
# Kill the process using port 8000 (Linux/macOS)
lsof -ti:8000 | xargs kill -9

# Or run on a different port
uvicorn app.main:app --port 8001
```

### Import errors

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
1. Ensure you're in the `backend` directory
2. Activate virtual environment
3. Run `pip install -r requirements.txt`

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Update models, schemas, repositories, routers
   - Write tests for new functionality
   - Follow existing code style

3. **Run tests:**
   ```bash
   pytest -v
   ```

4. **Create database migration (if needed):**
   ```bash
   alembic revision --autogenerate -m "Description"
   ```

5. **Test with the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Commit and push:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

7. **Create pull request on GitHub**

## Performance Considerations

- The application uses a single school record architecture
- Use connection pooling for production deployments
- Monitor database query performance with slow query logs
- Cache school data on frontend if appropriate
- Use CDN for logo_url images

## Security Notes

- Never commit `.env` or secrets to version control
- Rotate `SECRET_KEY` regularly in production
- Use HTTPS in production (handled by reverse proxy)
- Validate all input through Pydantic schemas
- Use strong database passwords
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Run `pip audit` to check for security vulnerabilities

## Contributing

1. Follow PEP 8 style guide
2. Add tests for new features
3. Run tests before submitting PR: `pytest`
4. Update documentation if needed

## License

Check project root for LICENSE file.

## Support

For issues and questions:
1. Check this README and troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed description

## Next Steps

- Add user authentication
- Add more endpoints (teachers, students, classes)
- Add file upload support for logos/documents
- Add email notifications
- Add admin dashboard
- Add analytics
