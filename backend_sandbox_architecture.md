# Architecture Specification: Backend Sandbox Execution Engine

## 1. System Overview
A distributed architecture utilizing a frontend web interface coupled with a Python-based API and a Dockerized execution sandbox. C++ scripts are executed on remote infrastructure.

## 2. Component Matrix

### 2.1. Frontend UI
*   **Framework:** JavaScript/TypeScript SPA (React/Next.js).
*   **Code Editor:** `monaco-editor`.
*   **Terminal Emulator:** `xterm.js` coupled with WebSockets for real-time bidirectional I/O streaming.

### 2.2. Backend API & Data Persistence
*   **Framework:** FastAPI (Python) or Node.js (Express).
*   **Database:** PostgreSQL or SQLite via SQL. Stores script metadata, source code blobs, execution logs, and script categorization.
*   **Connection Protocol:** HTTP REST for script retrieval; WebSockets for streaming execution I/O.

### 2.3. Execution Sandbox
*   **Containerization:** Docker daemon running on the host server.
*   **Environment:** Ephemeral Alpine Linux or minimal Debian containers with `g++` installed.
*   **Pipeline:**
    1. API receives execution request with script ID or raw code.
    2. API spawns a transient Docker container.
    3. Code is written to a temporary volume, compiled via `g++`, and executed.
    4. Container `stdout`/`stdin` streams are piped through the WebSocket back to the client.
    5. Container is forcibly destroyed (`--rm`) upon exit or timeout threshold.

## 3. Data Flow
1. Client requests script list from the Python SQL backend.
2. Client selects script; API serves raw C++ code to Monaco editor.
3. Client initiates execution over WebSocket connection.
4. Backend provisions a locked-down Docker container.
5. Bidirectional I/O streams between `xterm.js` and the executing C++ binary.
6. Execution terminates; socket closes; container is purged.

## 4. Security & Constraints
*   **Security:** High risk if misconfigured. Requires strict Docker isolation (no network access inside container, cgroups for memory/CPU limits, strict timeouts, non-root user execution).
*   **Constraints:** Introduces infrastructure costs, latency overhead, and database management responsibilities.

---

# Option 1: Portfolio MVP Start

## 1. Objective
Create a simpler, portfolio-ready version of the architecture with a strong visual result and a working C++ execution flow. The idea is to validate the main concept without building a full production system.

## 2. Recommended Stack
*   **Frontend:** React + Vite
*   **Code Editor:** Monaco Editor
*   **Backend:** FastAPI
*   **Database:** SQLite
*   **Sandbox Runtime:** Docker + g++
*   **Real-Time Terminal:** WebSocket + xterm.js

## 3. Scope of the MVP
This version should include:
*   A list of saved C++ scripts.
*   A code editor for writing and editing C++ code.
*   A Run button that triggers compilation and execution.
*   A terminal-like output area that shows compiler errors and program output.
*   A basic storage layer for script metadata and code.

## 4. MVP Architecture
### 4.1 Frontend
The frontend will be a single-page application with:
*   Sidebar or panel for script list.
*   Monaco editor area.
*   Execute button.
*   Terminal panel for stdin/stdout/stderr.
*   Save button for storing scripts.

### 4.2 Backend API
The backend exposes a small REST API:
*   `GET /scripts` - returns saved scripts
*   `GET /scripts/{id}` - returns a specific script
*   `POST /scripts` - creates or saves a script
*   `POST /execute` - receives code and returns execution results

### 4.3 Execution Pipeline
1. User clicks Run.
2. Frontend sends code to the FastAPI endpoint.
3. Backend creates a temporary Docker container.
4. Code is written to a temporary file.
5. Backend compiles with `g++`.
6. Program is executed inside the sandbox.
7. Output is streamed through WebSocket to the frontend.
8. Container is destroyed after execution or timeout.

### 4.4 Database Model
Use SQLite with a simple schema:
*   `id` - script identifier
*   `title` - script name
*   `code` - source code
*   `category` - optional classification
*   `created_at` - timestamp

## 5. Suggested Folder Structure
```text
project-root/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   └── database/
│   ├── requirements.txt
│   └── .env
├── sandbox/
│   ├── Dockerfile
│   ├── runner.sh
│   └── timeout.sh
├── db/
│   └── app.db
├── README.md
└── docker-compose.yml
```

## 6. Core Features to Prioritize
*   Fully working C++ compile and run flow.
*   Clean UI for editing code.
*   Real-time output streaming.
*   Timeout protection.
*   Simple script persistence.
*   Clear compile error handling.

## 7. Security for the MVP
Even in the portfolio version, keep the sandbox protected:
*   No network access in the container.
*   Short execution timeouts.
*   CPU and memory limit settings.
*   Automatic cleanup after run completion.
*   Execute as a non-root user whenever possible.

## 8. Why This Option Fits a Portfolio
This version is ideal for demonstrating:
*   Full-stack web development.
*   Backend API design.
*   Container-based execution.
*   Real-time application flows.
*   Security-aware engineering thinking.

## 9. Recommended Delivery Order
1. Build the frontend editor and terminal UI.
2. Connect the frontend to a FastAPI API.
3. Add SQLite persistence.
4. Implement Docker execution for C++ code.
5. Stream runtime output through WebSocket.
6. Add polish, examples, and documentation.

## 10. Final Recommendation
For a portfolio, this is the best first milestone because it balances ambition and feasibility. It is simple enough to finish, but impressive enough to demonstrate technical depth and practical engineering skills.

---

# Option 2: Production-Style Architecture

## 1. Objective
Create a more complete and scalable project structure that separates responsibilities clearly, improves security boundaries, and better reflects a real-world engineering system for running C++ code in a sandboxed environment.

## 2. Recommended Stack
*   **Frontend:** Next.js
*   **Code Editor:** Monaco Editor
*   **Backend API:** FastAPI
*   **Database:** PostgreSQL
*   **Execution Service:** Dedicated sandbox worker service
*   **Queue System:** Redis or Celery (optional but recommended)
*   **Real-Time Terminal:** WebSocket + xterm.js
*   **Container Runtime:** Docker

## 3. Target Architecture
This version uses a modular system with multiple services:
*   Web frontend for UI.
*   API backend for user and script management.
*   Execution worker for running code securely in containers.
*   Database for persistent storage.
*   Queue manager to handle jobs and concurrency.
*   Docker sandbox to compile and execute user code.

## 4. High-Level Flow
1. User logs in or accesses the app.
2. Frontend requests available scripts from the API.
3. User edits C++ code in Monaco.
4. User clicks Run.
5. API creates a job and stores execution metadata.
6. Worker pulls the job from the queue.
7. Worker starts a temporary container.
8. Code is compiled and executed.
9. Output is sent through WebSocket back to the user.
10. Logs and metadata are stored in PostgreSQL.
11. Container is cleaned up after completion.

## 5. Core Services
### 5.1 Frontend
*   Next.js web app.
*   Authentication and user session management.
*   Script editor and terminal UI.
*   History and execution monitoring page.

### 5.2 API Backend
*   REST endpoints for CRUD on scripts.
*   User management endpoints.
*   Execution request creation.
*   Job status endpoints.
*   WebSocket communication for live output.

### 5.3 Execution Worker
*   Receives execution requests from the queue.
*   Starts sandbox containers.
*   Compiles and runs C++ programs.
*   Captures stdout/stderr.
*   Enforces timeouts and limits.
*   Saves logs and exit status.

### 5.4 Database
Use PostgreSQL for:
*   users
*   scripts
*   execution jobs
*   logs
*   metadata
*   categories and tags

## 6. Recommended Folder Structure
```text
project-root/
├── apps/
│   ├── web/
│   │   ├── src/
│   │   ├── app/
│   │   ├── package.json
│   │   └── next.config.js
│   ├── api/
│   │   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── requirements.txt
│   └── worker/
│       ├── worker.py
│       ├── sandbox/
│       ├── config/
│       └── requirements.txt
├── packages/
│   └── shared/
│       ├── schemas/
│       └── types/
├── infra/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── postgres/
│   └── redis/
├── db/
│   └── init.sql
├── README.md
└── .env.example
```

## 7. Production Considerations
This version is better suited for:
*   multiple users
*   concurrency
*   monitoring
*   queue management
*   scaling future features
*   cleaner deployment pipelines

## 8. Security Controls
For a serious implementation, include:
*   Docker network isolation.
*   Resource quotas with cgroups.
*   Strict timeout enforcement.
*   Restricted filesystem access.
*   Non-root execution user.
*   Temporary workspace cleanup after each run.
*   Job-level logging and audit trails.

## 9. Suggested Features for This Version
*   Job queue and execution history.
*   Script categories and search filters.
*   User authentication and roles.
*   Execution status dashboard.
*   Automatic timeout and failure reporting.
*   Better monitoring and health checks.

## 10. Why This Option Is Stronger
This option demonstrates engineering maturity because it separates concerns and mirrors how a real application backend is structured in production. It is better for:
*   hiring signals
*   project credibility
*   future expansion
*   more robust deployment readiness

## 11. Recommended Delivery Order
1. Set up the Next.js frontend shell.
2. Build the FastAPI backend with script CRUD.
3. Add PostgreSQL models and migrations.
4. Create the job queue and worker service.
5. Add Docker sandbox execution.
6. Connect WebSocket streaming for terminal output.
7. Add monitoring, logs, and polished UI.

## 12. Best Use Case
Choose this option when you want a stronger, more professional portfolio project that looks like a real software platform rather than a simple prototype.

## 13. Final Recommendation
Option 2 is more complete and closer to a production product, but it requires more time and architecture work. It is the best choice if you want to showcase senior-level full-stack thinking and system design ability.

---

# Current Project Status

## 1. Selected Direction
We are building the project using Option 1: the portfolio MVP version.

## 2. Goal
Create a working full-stack app that allows a user to:
*   write C++ code in a browser editor,
*   save scripts,
*   compile and run them in a Docker sandbox,
*   view the terminal output in real time.

## 3. Current Focus
### Phase 1: Project foundation
*   Create the frontend app shell.
*   Set up the backend API.
*   Configure the SQLite database.
*   Define the project folder structure.

### Phase 2: Execution engine
*   Add Docker-based sandbox execution.
*   Compile C++ code using `g++`.
*   Capture stdout/stderr.
*   Enforce execution timeout.

### Phase 3: Real-time terminal
*   Connect the backend to the frontend through WebSocket.
*   Stream live output to the browser.
*   Show compile and runtime errors clearly.

### Phase 4: Polish and portfolio readiness
*   Improve styling.
*   Add example scripts.
*   Document setup steps.
*   Prepare the README for presenting the project.

## 4. Decision log
*   Chosen approach: Option 1 MVP.
*   Reason: Best balance of technical value and speed for portfolio presentation.
*   Stack: React + FastAPI + SQLite + Docker + g++ + WebSocket.

## 5. Next Immediate Tasks
1. Create the project folder structure.
2. Initialize the frontend app.
3. Initialize the backend API.
4. Add the SQLite model and database connection.
5. Build the first C++ execution test through Docker.
6. Connect the terminal output to the UI.

## 6. Notes
This document is the implementation record for the project. We should keep adding details as we build so the architecture, decisions, and progress remain clear and understandable.
