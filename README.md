# Task-Management

# Async Task Management API

A high-performance RESTful API built with **FastAPI**, **PostgreSQL (Async)**, and **Docker**. 
Designed for scalability using Layered Architecture and Dependency Injection.

## 🚀 Features Implemented

### 1. Core Architecture
- **Layered Design:** Strict separation of concerns (API -> Service -> Repository).
- **Async Database:** Uses `asyncpg` + `SQLAlchemy` for non-blocking I/O.
- **Dependency Injection:** Repositories are injected into Services, making unit testing easy.

### 2. Product Features (SDE-2 Requirements)
I selected the following advanced features to demonstrate handling complex data relationships and dynamic querying:

* **Task Dependencies (Graph Logic):** * *Why:* Demonstrates ability to handle self-referential database relationships and enforce business integrity rules (preventing tasks from closing prematurely).
    * *Logic:* A Many-to-Many self-referential relationship blocks a task from being marked `DONE` if any of its `blocking_tasks` are not `DONE`.

* **Advanced Filtering:** * *Why:* Essential for frontend dashboards (e.g., Kanban boards).
    * *Logic:* Implemented a dynamic query builder in the Repository layer to filter by multiple optional criteria (Status, Priority) without writing messy `if/else` SQL chains.

## 🛠 Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (v15)
- **ORM:** SQLAlchemy (Async)
- **Migrations:** Alembic
- **Auth:** JWT (OAuth2)
- **Containerization:** Docker & Docker Compose

## 🏃‍♂️ How to Run

1. **Start Infrastructure:**
   ```bash
   docker-compose up -d

2.  **Run Migration:**
    ```bash
    alembic upgrade head

3. **Start Server:**
   ```bash
   uvicorn main:app --reload

4. **API Endpoints:**
   ```bash
   http://127.0.0.1:8000/docs
