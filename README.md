# Fenmo Expense Tracker

A minimal full-stack expense tracking application built with FastAPI and Streamlit.

This tool allows users to record, view, filter, and analyze personal expenses in a reliable and production-like manner.

---

## 🚀 Live Demo

Frontend: https://fenmo-expense-tracker-bp5hbnvtqhahazls3wtkp6.streamlit.app/  
Backend API: https://fenmo-expense-tracker.onrender.com

---

## ✨ Features

- Add new expenses with amount, category, description, and date
- View all recorded expenses
- Filter by category
- Sort by newest date
- View total of visible expenses
- Summary view (total per category)
- Retry-safe API using idempotency keys
- Basic input validation
- Error and loading states

---

## 🛠️ Tech Stack

- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: Streamlit
- Language: Python
- Deployment: Render (API), Streamlit Cloud (UI)

---

## 📐 System Design

### Backend

- REST API built using FastAPI
- SQLite used for lightweight persistence
- SQLAlchemy ORM for database interaction
- Idempotency implemented using `X-Request-ID` header
- Decimal used for accurate money handling

### Frontend

- Streamlit-based web UI
- Communicates with backend via REST APIs
- Implements loading and error states
- Client-side validation
- Summary analytics

---

## 🧪 Testing

Basic automated tests were written to validate:

- Retry safety
- Duplicate request handling
- API resilience

Tests are available in `test_api.py`.

---

## ⚖️ Design Decisions

- Used FastAPI for clear API contracts, automatic validation, and API documentation.
- Chose SQLite for lightweight persistence and minimal setup overhead.
- Implemented idempotency using X-Request-ID headers to safely handle retries.
- Used Decimal types for accurate handling of monetary values.
- Built the UI using Streamlit for rapid development and deployment.

---

## 🔁 Trade-offs

- Implemented a single-user system without authentication.
- Used SQLite instead of a managed database service.
- Limited UI styling in favor of functional clarity.
- Did not implement pagination for large datasets.

These choices allowed prioritization of correctness, reliability, and deployment within the timebox.

---

## ❌ Not Implemented

- User accounts and authentication flows.
- Data export and reporting features.
- Advanced analytics and visualizations.
- Mobile-first responsive design.

These were consciously excluded to focus on core system behavior and stability.

---

## Future Improvements

- Add user authentication and multi-user support
- Migrate to PostgreSQL for scalability
- Add pagination and indexing
- Introduce background jobs for reporting
- Improve monitoring and logging


## 🏃 Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
