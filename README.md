# 🚀 Nexus AI Investment Research Dashboard

Nexus is a premium SaaS application that acts as an **AI-powered financial research assistant**, capable of dynamically gathering market data, synthesizing insights, and presenting structured investment analysis in real time.

---

## 🧠 Problem Statement

Retail investment tools today fall into two extremes:

* Too simplistic → lack actionable insights
* Too complex → require expertise (e.g., Bloomberg Terminal)

Nexus bridges this gap by:

* Automating data collection (prices, news, context)
* Using AI to synthesize insights
* Delivering structured, readable outputs in a modern SaaS UI

---

## ✨ Core Features

### 🔹 Intelligent AI Orchestration

Natural language queries trigger automated tool execution (stock data, news, internal knowledge base).

### 🔹 Structured Knowledge Delivery

AI responses are returned as **strict JSON schemas**, directly mapped to UI components (not raw chat).

### 🔹 Source Attribution

All generated insights include references to improve trust and transparency.

### 🔹 Multi-Tenant SaaS Architecture

* JWT-based authentication
* Organization-level data isolation
* Secure multi-user support

### 🔹 Premium UX

* Glassmorphic UI
* Dark mode
* Micro-interactions
* Built using Tailwind CSS + modern component patterns

---

## 📊 Observability & Monitoring (NEW)

This project includes a full **monitoring stack**:

* **Prometheus** → Scrapes backend metrics
* **Grafana** → Visualizes system performance
* **Custom Metrics**:

  * `request_count_total`
  * `request_latency_seconds`
  * API health (`up`)

### Monitoring Flow:

Flask API → `/metrics` → Prometheus → Grafana Dashboard

---

## 🛠 Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS v3
* React Router

### Backend

* Flask
* SQLAlchemy
* JWT Authentication

### Database

* SQLite (local)
* PostgreSQL (Supabase-ready)

### AI & Data

* OpenAI API (tool calling)
* yfinance

### DevOps / Monitoring

* Docker & Docker Compose
* Prometheus
* Grafana

---

## 🏗 Architecture Overview

The system follows a **decoupled microservice-style architecture**:

1. Frontend sends authenticated request (JWT)
2. Flask backend validates user + tenant
3. `ai_orchestrator` determines required tools
4. External data is fetched (APIs, services)
5. LLM generates structured JSON output
6. Response stored in DB and returned to UI

---

## ⚙️ Setup Instructions

### 🔹 Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

### 🔹 Frontend

```bash
cd frontend
npm install
npm run dev
```

---

### 🔹 Run Full Stack (Docker)

```bash
docker-compose up --build
```

---

## 📊 Monitoring Queries (Prometheus & Grafana)

Below are the core queries used to monitor application performance:

### 🔹 1. Service Health Check

Checks whether the Flask service is up.

```promql
up{job="flask-app"}
```

---

### 🔹 2. Total API Requests

Tracks the total number of API calls handled.

```promql
request_count_total
```

---

### 🔹 3. Request Rate (Traffic)

Shows how many requests are being processed per second.

```promql
rate(request_count_total[1m])
```

---

### 🔹 4. Request Volume (Stable for Bursts)

Useful when traffic is not continuous.

```promql
increase(request_count_total[5m])
```

---

### 🔹 5. Average Request Latency

Measures how long requests take on average.

```promql
rate(request_latency_seconds_sum[1m]) 
/
rate(request_latency_seconds_count[1m])
```

---

### 🔹 6. Total Requests Across All Instances

Aggregated metric ignoring labels.

```promql
sum(request_count_total)
```

---

### 📈 Notes

* `rate()` is used for continuous traffic analysis
* `increase()` is more reliable for burst traffic
* Latency is calculated using histogram sum/count

These queries are visualized in Grafana dashboards for real-time observability.

---

## 🔐 Environment Variables

```
OPENAI_API_KEY=your_key_here
SECRET_KEY=jwt_secret
DATABASE_URL=sqlite:///local_db.sqlite3
```

---

## 🌐 Services

| Service     | URL                   |
| ----------- | --------------------- |
| Frontend    | http://localhost:5173 |
| Backend API | http://localhost:5001 |
| Prometheus  | http://localhost:9090 |
| Grafana     | http://localhost:3000 |

---

## 📈 Sample Metrics

* API request volume
* Request latency
* Service uptime

---

## 🚀 Deployment Targets

* Frontend → Vercel
* Backend → Render
* Database → Supabase
* Monitoring → Docker on EC2 (planned)

---

## ⚠️ Known Limitations

* Knowledge base is currently mocked
* News API responses are simulated
* No vector database integration yet

---

## 🔮 Future Improvements

* Vector DB integration (pgvector / Pinecone)
* Real-time news APIs (NewsAPI / AlphaVantage)
* Alerting system (Grafana alerts)
* CI/CD pipeline (GitHub Actions)
* Full AWS deployment (EC2 + Docker)

---

## 🧠 Key Highlights

* AI-driven backend orchestration
* Production-style monitoring with Prometheus + Grafana
* Multi-tenant SaaS-ready architecture
* Clean separation of frontend, backend, and AI logic

---

## 💡 Author

Tanya Singh
Computer Science | Cloud & DevOps Focus
