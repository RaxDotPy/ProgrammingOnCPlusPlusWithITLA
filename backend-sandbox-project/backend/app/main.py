from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.db import get_connection, init_db

app = FastAPI(title="C++ Sandbox Runner")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScriptCreate(BaseModel):
    title: str
    code: str
    category: str = "general"


class ScriptExecute(BaseModel):
    title: str
    code: str


def collect_cpp_source_files(base_dir: str | os.PathLike[str] = SRC_ROOT):
    root = Path(base_dir)
    if not root.exists():
        return []

    files = []
    for file_path in sorted(root.rglob("*.cpp")):
        if file_path.is_file():
            rel_path = file_path.relative_to(root).as_posix()
            try:
                code = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                code = file_path.read_text(encoding="latin-1", errors="ignore")

            files.append(
                {
                    "title": file_path.stem,
                    "path": rel_path,
                    "code": code,
                    "full_path": str(file_path),
                }
            )

    return files


def find_compiler():
    candidates = [
        shutil.which("g++"),
        shutil.which("clang++"),
        r"C:\Users\diose\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260616-ucrt-x86_64\bin\g++.exe",
        r"C:\Users\diose\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260616-ucrt-x86_64\bin\clang++.exe",
    ]

    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate

    raise RuntimeError("C++ compiler not found. Install MinGW or use the Docker sandbox target environment.")


def build_runtime_env():
    compiler_path = find_compiler()
    compiler_dir = os.path.dirname(compiler_path)
    env = os.environ.copy()
    path_value = env.get("PATH", "")
    env["PATH"] = compiler_dir + os.pathsep + path_value if compiler_dir not in path_value else path_value
    return env


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/scripts")
def list_scripts():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, title, code, category, created_at FROM scripts ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.get("/source-files")
def list_source_files():
    return collect_cpp_source_files(SRC_ROOT)


@app.get("/source-files/content")
def read_source_file(path: str):
    source_root = SRC_ROOT.resolve()
    target = (source_root / Path(path)).resolve()

    if not str(target).startswith(str(source_root)):
        return {"success": False, "error": "Invalid source path."}

    if not target.exists() or not target.is_file():
        return {"success": False, "error": "File not found."}

    try:
        code = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        code = target.read_text(encoding="latin-1", errors="ignore")

    return {
        "success": True,
        "title": target.stem,
        "path": target.relative_to(source_root).as_posix(),
        "code": code,
    }


@app.post("/scripts")
def create_script(script: ScriptCreate):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO scripts (title, code, category, created_at) VALUES (?, ?, ?, ?)",
            (script.title, script.code, script.category, datetime.utcnow().isoformat()),
        )
        conn.commit()
        script_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, title, code, category, created_at FROM scripts WHERE id = ?",
            (script_id,),
        ).fetchone()
        return dict(row)
    finally:
        conn.close()


@app.post("/execute")
def execute_script(script: ScriptExecute):
    try:
        compiler = find_compiler()
    except RuntimeError as exc:
        return {
            "success": False,
            "output": str(exc),
            "type": "environment_error",
        }

    with tempfile.TemporaryDirectory(prefix="cpp_run_") as temp_dir:
        source_path = os.path.join(temp_dir, "main.cpp")
        exe_path = os.path.join(temp_dir, "app")

        with open(source_path, "w", encoding="utf-8") as file:
            file.write(script.code)

        runtime_env = build_runtime_env()

        try:
            compile_result = subprocess.run(
                [compiler, source_path, "-std=c++17", "-O2", "-static", "-o", exe_path],
                capture_output=True,
                text=True,
                timeout=15,
                env=runtime_env,
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "Compilation timed out after 15 seconds.",
                "type": "timeout",
            }

        if compile_result.returncode != 0:
            return {
                "success": False,
                "output": compile_result.stderr.strip() or compile_result.stdout.strip(),
                "type": "compile_error",
            }

        try:
            run_result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                timeout=10,
                env=runtime_env,
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "Program execution timed out after 10 seconds.",
                "type": "timeout",
            }

        return {
            "success": run_result.returncode == 0,
            "output": (run_result.stdout + run_result.stderr).strip(),
            "type": "execution_result",
            "exit_code": run_result.returncode,
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
