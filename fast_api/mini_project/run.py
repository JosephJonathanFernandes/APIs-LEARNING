"""
Run the FastAPI application
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)