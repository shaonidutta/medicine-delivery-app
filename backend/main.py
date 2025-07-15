"""
Production entry point for Render deployment
"""

# Import the FastAPI app directly so Render can find it
from app.main import app

# This makes the app available as main:app for uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    print("🚀 Starting Quick Commerce Medicine Delivery API...")
    print(f"📍 Server: {host}:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"🏥 Health: http://localhost:{port}/health")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
