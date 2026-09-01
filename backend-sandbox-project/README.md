# C++ Sandbox Runner

A full-stack web application that lets you write, save, and execute C++ code from a browser-based editor. Features a searchable file browser with 94+ programming exercises and assignments.

## ✨ Features

- **Code Editor** - Edit C++ code in a browser-based editor
- **File Browser** - Browse and search 94+ .cpp files from a project source directory
- **Real-time Compilation** - Compile C++ code with g++ and see compiler errors
- **Program Execution** - Run compiled programs and capture output
- **Save/Load Scripts** - Save custom scripts to SQLite and reload them
- **Search Functionality** - Find files by name or path in real-time
- **Clean UI** - Dark-themed, professional interface optimized for coding

## 🛠️ Tech Stack

**Frontend**
- React 18
- Vite (build tool)
- CSS3 (dark theme styling)

**Backend**
- FastAPI (Python web framework)
- Uvicorn (ASGI server)
- SQLite (persistent storage)
- MinGW/LLVM (C++ compiler)

## 📋 Prerequisites

### Required Software
- **Python 3.11+** - For running the FastAPI backend
- **Node.js 18+** - For running React frontend and npm
- **C++ Compiler** - Either:
  - MinGW (Windows): Download from [LLVM MinGW](https://github.com/mstorsjo/llvm-mingw/releases)
  - GCC/Clang (Linux/Mac): Already installed or installable via package manager

### Verify Installations
```bash
python --version     # Should show Python 3.11+
node --version       # Should show Node 18+
npm --version        # Should show npm 9+
g++ --version        # Should show a compiler version (or install MinGW)
```

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

**Backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend dependencies:**
```bash
cd ../frontend
npm install
```

### Step 2: Start the Backend Server

Open a terminal and run:
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Step 3: Start the Frontend Server

Open a second terminal and run:
```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

You should see:
```
VITE v5.4.21  ready in XXX ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://10.0.0.X:5173/
```

### Step 4: Open the App

Open your browser and navigate to:
```
http://localhost:5173
```

## 📖 How to Use

### 1. Browse and Load Source Files
- Look at the left sidebar - you'll see a list of .cpp files from the `src/` folder
- Type in the search box to filter files by name (e.g., "Operadores", "ejercicio")
- Click any file to load its code into the editor

### 2. Write or Edit Code
- Edit the code in the editor on the right
- Or load one of the provided exercises
- Change the script name if desired

### 3. Run Your Code
- Click the "Run" button
- The backend will:
  1. Compile the C++ code with g++
  2. Execute the compiled program
  3. Capture and display the output
- You'll see the status and output in the console panel below the editor

### 4. Save Your Work
- Modify a script name and click "Save script"
- Your custom scripts appear in the lower section of the sidebar
- Click saved scripts anytime to reload them

## 📁 Project Structure

```
backend-sandbox-project/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, execution engine
│   │   ├── db.py                # SQLite database setup
│   │   └── __init__.py
│   ├── requirements.txt          # Python dependencies
│   └── tests/
│       └── test_source_files.py  # Unit tests
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── styles.css           # UI styling
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json             # npm dependencies
│   ├── vite.config.js           # Vite configuration
│   └── dist/                    # Production build (after npm run build)
├── src/                         # All .cpp source files (94 files)
│   ├── ejercicios con funciones/  # 40 function exercise files
│   ├── ejercicios con struct/     # 10 struct exercise files
│   ├── practica videos/           # 3 practice files
│   └── [root level .cpp files]    # Operators, POO, activities, etc.
├── db/
│   └── app.db                   # SQLite database (created on first run)
├── sandbox/
│   ├── Dockerfile               # Docker container definition
│   └── run.sh                   # Sandbox execution script
├── docker-compose.yml           # Docker Compose configuration
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

All endpoints run on `http://localhost:8000`

### Health Check
- `GET /health` - Check if backend is running

### Source File Management
- `GET /source-files` - List all .cpp files from src/ folder
- `GET /source-files/content?path=<filename>` - Load a specific file's code

### Script Management (User-saved scripts)
- `GET /scripts` - List all saved scripts
- `POST /scripts` - Save a new script
  ```json
  { "title": "my script", "code": "...", "category": "general" }
  ```

### Code Execution
- `POST /execute` - Compile and run C++ code
  ```json
  { "title": "my script", "code": "#include <iostream>\nint main() { ... }" }
  ```
  Returns:
  ```json
  {
    "success": true,
    "output": "program output here",
    "type": "execution_result",
    "exit_code": 0
  }
  ```

## 🧪 Example: Running an Exercise

1. **Load "Operadores aritmeticos.cpp"** from the file browser
2. **Click Run**
3. **See Output:**
   ```
   Suma: 27
   Resta: 13
   Multiplicación: 140
   División: 2
   Módulo: 6
   ```

## ⚙️ Troubleshooting

### "Port 8000 already in use"
- Another process is using port 8000
- Kill it: `lsof -ti:8000 | xargs kill -9` (Linux/Mac) or `Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process` (Windows)
- Or use a different port: `python -m uvicorn app.main:app --port 8001`

### "Port 5173 already in use"
- Kill the process on that port or use: `npm run dev -- --host 0.0.0.0 --port 5174`

### "g++/clang++ not found"
- Install MinGW/LLVM-MinGW: `winget install MartinStorsjo.LLVM-MinGW.UCRT`
- Or install GCC on Linux: `sudo apt-get install build-essential`
- Or install on Mac: `brew install gcc`

### "No .cpp files found in src"
- Ensure the `src/` folder exists in the project root
- Copy your .cpp files into it
- Restart the backend (it auto-reloads with `--reload`)

### Backend not responding
- Check that `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000` is running
- Check the terminal for error messages
- Verify Python 3.11+ is installed: `python --version`

### Frontend not loading
- Check that `npm run dev -- --host 0.0.0.0` is running
- Verify Node.js is installed: `node --version`
- Try clearing browser cache (Ctrl+Shift+Delete)

## 📦 Installation Detailed Walkthrough

### For Windows

1. **Install Python 3.11+**
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Install Node.js 18+**
   - Download from https://nodejs.org/
   - Use LTS version (18.x or 20.x)

3. **Install MinGW Compiler**
   ```bash
   winget install MartinStorsjo.LLVM-MinGW.UCRT
   ```

4. **Navigate to project directory**
   ```bash
   cd "path\to\backend-sandbox-project"
   ```

5. **Install Python packages**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

6. **Install Node packages**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### For Linux

1. **Install Python, Node.js, and GCC**
   ```bash
   sudo apt-get update
   sudo apt-get install python3.11 python3-pip nodejs npm build-essential
   ```

2. **Navigate to project directory**
   ```bash
   cd /path/to/backend-sandbox-project
   ```

3. **Install dependencies**
   ```bash
   cd backend && pip install -r requirements.txt && cd ..
   cd frontend && npm install && cd ..
   ```

### For macOS

1. **Install via Homebrew**
   ```bash
   brew install python@3.11 node gcc
   ```

2. **Navigate to project directory**
   ```bash
   cd /path/to/backend-sandbox-project
   ```

3. **Install dependencies**
   ```bash
   cd backend && pip install -r requirements.txt && cd ..
   cd frontend && npm install && cd ..
   ```

## 🏗️ Production Build

To create an optimized production build of the frontend:

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized HTML, CSS, and JavaScript files ready for deployment.

## 📝 Development Notes

- The backend uses **auto-reload** mode (`--reload` flag), so changes to Python files automatically restart the server
- The frontend uses **Vite HMR** (Hot Module Replacement), so React changes appear instantly in the browser
- SQLite database is created automatically on first run in `db/app.db`
- The `src/` folder can contain unlimited .cpp files organized in subdirectories

## 🎯 Use Cases

- **Learning**: Browse and run 94+ C++ programming exercises
- **Practice**: Write and test your own C++ code in the browser
- **Teaching**: Share exercises and solutions with students
- **Portfolio**: Demonstrate full-stack development skills with this project
- **Prototyping**: Quick compilation and testing of C++ snippets

## 📚 About the Source Files

The project includes 94 C++ files from a comprehensive "Fundamentos de Programacion" (Programming Fundamentals) course:

- **Operators** (Operadores): arithmetic, assignment, comparison, logical operators
- **Data Types**: variables, constants, char, float, double
- **Control Flow**: if/else statements, loops
- **Functions**: 40 exercises with functions
- **Arrays** (Arreglos): 3+ array manipulation exercises
- **Structs**: 10+ exercises with structures
- **OOP**: Classes, constructors, destructors, getters, setters, encapsulation
- **Activities**: Professor assignments and practice exercises

## 📄 License

This is a portfolio project. Feel free to use it as a learning resource or portfolio piece.

## ✉️ Questions?

Refer to the API documentation above or check the backend logs (`INFO:` messages in the terminal) when running the server.

---

**Last Updated:** September 1, 2026
**Status:** ✅ Fully functional and tested with 94 source files
