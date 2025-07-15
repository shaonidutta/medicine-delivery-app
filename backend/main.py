"""
Production entry point for Render deployment
"""

import uvicorn
import os

def main():
    """Main entry point"""
    try:
        from app.main import app
        print("✅ App imported successfully!")
        print(f"App title: {app.title}")

        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"

        print(f"🚀 Starting server on {host}:{port}")
        print(f"📚 API Documentation: http://localhost:{port}/docs")
        print(f"🏥 Health Check: http://localhost:{port}/health")

        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
