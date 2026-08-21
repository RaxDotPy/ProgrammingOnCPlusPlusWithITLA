# C++ Sandbox Runner

A compact full-stack portfolio project that lets a user write, save, and execute C++ code from a browser-based editor.

## Highlights
- React frontend with a simple code editor
- FastAPI backend for script management and execution
- SQLite storage for saved scripts
- Compile and execution flow for C++ with output capture
- Clean, demo-friendly UI for a portfolio presentation

## Stack
- React + Vite
- FastAPI
- SQLite
- MinGW-based local compiler for the prototype
- Docker-based design target for the production version

## Intended workflow
1. Open the browser app
2. Write or edit C++ code
3. Click Run
4. The backend compiles the source
5. The result is returned to the UI console

## Project structure
- frontend: React app
- backend: FastAPI app and database access
- src: organized C++ source files that the app can browse and execute
- sandbox: docker and execution script files
- db: SQLite database

## Source browser workflow
1. Place C++ files inside the src folder
2. Open the app in the browser
3. Search for a file by name or path in the sidebar
4. Click a file to load it into the editor
5. Run it directly from the app

## Local setup
1. Open a terminal in the backend folder
2. Run the API server:
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
3. Open a second terminal in the frontend folder
4. Start the React app:
   npm run dev -- --host 0.0.0.0
5. Open the app at http://localhost:5173

## Notes
This is a working prototype built to showcase competence in full-stack development, backend APIs, and runtime execution handling. The architecture remains aligned with the original sandbox concept, while the local implementation uses a simpler compiler setup to keep the demo practical on a standard machine.
