# School Website

A simple modular-monolith web application for a school website, designed for a small public-facing site with an administrator workflow.

## Stack

- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic

## Project structure

- `frontend/` — React frontend application
- `backend/` — FastAPI backend application
- `.env.example` — environment variables template

## Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL running locally

## Frontend setup

1. Open a terminal in the project root.
2. Install dependencies:
   npm install --prefix frontend
3. Start the dev server:
   npm run dev --prefix frontend
4. Open the local URL shown in the terminal, typically http://localhost:5173.

## Backend setup

1. Open a terminal inside the `backend/` folder.
2. Create and activate a virtual environment:
   python -m venv .venv
   .venv\Scripts\activate
3. Install Python dependencies:
   python -m pip install -r requirements.txt
4. Create your local environment file from the template:
   copy .env.example .env
5. Start the API:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Notes

- This scaffold intentionally contains no business features yet.
- Authentication, database tables, and feature implementations are intentionally not included in this phase.
- The backend is structured to allow future feature modules without a full rewrite.
