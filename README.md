# Nexus AI Investment Research Dashboard

Nexus is a premium SaaS application designed to act as an AI-powered financial researcher. It dynamically pulls real-time stock data and simulated news to provide structured AI-driven company analyses on demand.

## Problem Statement
Traditional retail investment tools are either too simplistic or wildly complex (like Bloomberg Terminals). Users spend hours gathering earnings reports, stock charts, and news manually. Nexus bridges this gap by using AI to autonomously gather, synthesize, and structure this data into readable insights, wrapped in a beautiful, consumer-grade SaaS interface.

## Features
- **Intelligent Orchestration**: Conversational query translates to automated tool-calling (stock pricing, news, knowledge-base search).
- **Structured Knowledge Delivery**: The AI doesn't return raw chat text. It returns rigorous JSON structures mapped directly to the UI elements.
- **Source Attribution**: Every piece of data is sourced, increasing user trust.
- **SaaS First**: Full multi-tenancy implementation using JWTs and Organizational ID filtering, ready for onboarding distinct teams securely.
- **Premium UX**: Glassmorphic interfaces, dark mode, micro-animations, built on Tailwind CSS + shadcn/ui principles.

## Tech Stack
- Frontend: Vite, React, Tailwind CSS v3, React Router
- Backend: Flask, SQLAlchemy, JWT Authentication
- Database: SQLite (local fallback), ready for Supabase (PostgreSQL)
- AI Ops: OpenAI Tool Calling API (gpt-3.5-turbo), yfinance

## Architecture Summary
The frontend is completely decoupled from the AI and the data structures. It communicates securely via JWTs over REST over to the Flask backend.
The Flask backend intercepts the request, checks multi-tenant permissions, and kicks off the `ai_orchestrator`.
The Orchestrator determines which external resources the prompt needs (using OpenAI Functions), executes pure python calls, and aggregates the context back to the LLM. The LLM produces a unified JSON payload, which is stored in the relational database, and passed back to the frontend.

## Setup Instructions

**Backend**
1. `cd backend`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Define `.env` with `OPENAI_API_KEY=sk-...` (or leave empty to trigger mock responses)
5. `python app.py`

**Frontend**
1. `cd frontend`
2. `npm install`
3. `npm run dev`

Alternatively, use **Docker**:
`docker-compose up --build`

## Environment Variables
- `OPENAI_API_KEY`: Required for real AI synthesis.
- `SECRET_KEY`: JWT Signing Key.
- `DATABASE_URL`: URI for PostgreSQL (Defaults to local `sqlite:///local_db.sqlite3`).

## Deployment Links
*Frontend target: Vercel*
*Backend target: Render*
*Database target: Supabase*
*(Deployment instances to follow in live demo)*

## Known Limitations & Future Improvements
- The current knowledge-base search is statically mocked. Future improvement: Connect to a vector database (e.g., Pinecone/Supabase pgvector) and ingest PDF earnings automatically via a cron job.
- News search currently outputs generic mocked text. Future improvement: wire up to AlphaVantage or NewsAPI.
