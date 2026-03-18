@echo off
REM Windows development startup script

echo Starting FastAPI development server on Windows...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
uvicorn app.main:app --reload

REM Deactivate on exit
deactivate
