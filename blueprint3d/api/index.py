"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from fastapi.responses import JSONResponse

# Vercel requires a handler function
def handler(request):
    """
    Vercel serverless function handler
    """
    return JSONResponse({
        "message": "API is running",
        "docs": "/docs"
    })