# PowerShell launcher for Veritas
Write-Host "========================================================" -ForegroundColor DarkGreen
Write-Host "  Starting Veritas — Causal Synthetic Data Platform" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor DarkGreen

Write-Host "Launching Backend (FastAPI on http://127.0.0.1:8000)..." -ForegroundColor Cyan
Start-Process python -ArgumentList "backend\run.py"

Write-Host "Launching Frontend (Vite on http://localhost:5173)..." -ForegroundColor Cyan
Start-Process npm -ArgumentList "run dev" -WorkingDirectory "frontend"

Write-Host "`nPlatform running successfully!" -ForegroundColor Green
Write-Host "Open your browser to: http://localhost:5173" -ForegroundColor Yellow
Write-Host "API Swagger documentation: http://127.0.0.1:8000/docs" -ForegroundColor Gray
