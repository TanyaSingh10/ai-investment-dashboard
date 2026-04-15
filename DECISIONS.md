# Project Decisions & Trade-Offs

## Why this project?
An AI Investment Research Dashboard perfectly intersects complex domain logic (finance) with modern AI capabilities (tool-using LLMs) and deep backend principles (multi-tenancy, structured data APIs). It directly highlights production capabilities that companies value over generic "chatbots."

## Why this tech stack?
- **React/Vite**: The industry standard for robust, components-based frontends. Vite provides the speed needed for tight feedback loops.
- **Flask**: Lightweight and expressive. Ideal for microservices that handle AI pipelines where heavy frameworks (like Django) might introduce unnecessary overhead for simple REST APIs.
- **PostgreSQL / Supabase**: Excellent support for JSONB (required for dynamic AI payloads) while strictly maintaining relational integrity.

## Multi-Tenancy Approach
We enforce multi-tenancy at the application layer via `org_id`.
Every table containing user-generated data (`users`, `reports`) possesses an `org_id` foreign key.
The Flask middleware decodes the JWT, extracts `g.org_id`, and explicitly appends `.filter_by(org_id=g.org_id)` on all database CRUD operations. This ensures complete data isolation without the overhead of separate databases per tenant.

## AI Design Decisions
A deliberate decision was made to *avoid* heavy generic agent frameworks (like Autogen or complex Langchain sequences).
Instead, we utilize the native OpenAI Tool Calling API in a clean, functional abstraction. 
This provides:
1. Predictability
2. Massive reduction in latency
3. Easier debugging (the exact JSON tree is transparent)

## Trade-offs
- **SQLite Fallback**: For immediate peer review and testing, SQLite is the default. SQLite does not natively support strict JSONB operations like PostgreSQL does, so we fell back to a regular `JSON/Text` column implementation for the MVP.
- **Mocking external APIs**: Calling out to paid news feeds adds friction to the build setup. Native mocked python functions handle the endpoints unless explicitly coded, prioritizing UX and architecture over scraping integrity for the prototype.
