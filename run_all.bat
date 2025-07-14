@echo off

REM Start the backend
start "Backend Server" cmd /k ".\run_backend.bat"

REM Wait for a few seconds to ensure the backend starts up
ping 127.0.0.1 -n 5 > nul

REM Start the frontend
start "Frontend App" cmd /k "cd src\frontend\frontend-app && npm run dev"