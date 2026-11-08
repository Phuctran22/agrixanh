@echo off
title AgriXanh Backend (FastAPI)
echo ==============================================
echo   AgriXanh Backend API Server (Port 8000)
echo ==============================================
cd /d "%~dp0backend"
py -3.12 -m uvicorn main:app --reload --port 8000
pause
