@echo off
echo ========================================================
echo   Starting Veritas — Causal Explainable Synthetic AI
echo ========================================================

echo Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "Veritas Backend" cmd /k "python backend\run.py"

echo Starting Vite React Frontend on http://localhost:5173 ...
cd frontend
start "Veritas Frontend" cmd /k "npm run dev"

echo.
echo ========================================================
echo   Veritas is launching!
echo   Frontend: http://localhost:5173
echo   Backend Docs: http://127.0.0.1:8000/docs
echo ========================================================
pause
