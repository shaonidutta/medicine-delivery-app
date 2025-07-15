#!/usr/bin/env python3
"""
Simple server runner to test the backend
"""

import sys
import os

def main():
    print("🔧 Quick Commerce Medicine Delivery API")
    print("=" * 50)
    
    # Test imports
    print("📋 Testing imports...")
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully!")
        
        import uvicorn
        print("✅ Uvicorn imported successfully!")
        
        # Get port from environment or use default
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        
        print(f"🚀 Starting server on http://{host}:{port}")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🏥 Health Check: http://localhost:8000/health")
        print("=" * 50)
        
        # Start the server
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
