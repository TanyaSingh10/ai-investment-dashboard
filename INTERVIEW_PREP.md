# Interview Preparation Guide

This document is specialized to help you explain the architecture and design of this project during your internship interview.

## Explaining the Architecture Simply
"I built a decoupled SaaS application. The frontend is a React SPA focused purely on presentation. The heavy lifting is done by the Flask backend which acts as an orchestrator. When a user asks a question, the backend doesn't just hit an LLM. It hits an AI Orchestrator that figures out what tools it needs—say, the yfinance API to get stock data. It writes python code behind the scenes to fetch that data, feeds it back to the LLM, and explicitly forces the LLM to return a highly structured JSON object, preventing hallucination. Finally, it securely saves this JSON for the user's specific organization and sends it back to the frontend to render."

## Common Questions & Answers

**Q: How did you handle security and user data separation?**
> A: "I implemented a multi-tenant model. When a user logs in, the JWT issued contains their `org_id`. A custom middleware wrapper in Flask extracts this ID and attaches it to the global request object. Every single database query strictly filters by this `org_id`. A user from Org A literally cannot query a report from Org B because the API completely blocks it at the ORM level."

**Q: Why didn't you just let the AI talk directly to the frontend?**
> A: "Security and stability. The frontend should never hold API keys. By putting the AI in the backend, I maintain control over the cost (rate limiting), I ensure the AI accesses the database securely as a proxy, and I can strictly enforce a JSON Schema output so the frontend doesn't break trying to parse raw text."

**Q: Explain how the AI orchestration works without a massive framework.**
> A: "I used OpenAI's native function calling functionality. I defined python dictionaries that describe functions like `get_stock_data`. The LLM decides what to call, returns the function name to python, python actually runs the function securely, and passes the result back. It's incredibly fast, requires zero dependencies beyond the standard OpenAI SDK, and is completely transparent."

**Q: What would you change if you had more time?**
> A: "I would swap the local mock knowledge base for a vector store like PGVector inside Supabase, and implement RAG (Retrieval-Augmented Generation) so the AI could automatically cite specific paragraphs from uploaded 10-K PDFs."
