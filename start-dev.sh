#!/bin/bash
# Mac/Linux development startup script

echo "Starting FastAPI development server on Mac/Linux..."

# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn app.main:app --reload

# Deactivate on exit
deactivate
