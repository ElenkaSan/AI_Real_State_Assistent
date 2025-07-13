#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running FastAPI app with auto-reload..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000