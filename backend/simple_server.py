#!/usr/bin/env python3
"""
Simple FastAPI server to test basic functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_simple_app():
    """Create a minimal FastAPI app for testing"""
    try:
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
        
        app = FastAPI(
            title="Quick Commerce Medicine Delivery API",
            description="Medicine delivery service API",
            version="1.0.0"
        )
        
        @app.get("/")
        async def root():
            return {"message": "Quick Commerce Medicine Delivery API", "status": "running"}
        
        @app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "medicine-delivery-api"}
        
        @app.get("/test")
        async def test_endpoint():
            return {
                "message": "Test endpoint working",
                "python_version": sys.version,
                "status": "success"
            }
        
        return app
        
    except Exception as e:
        print(f"❌ Error creating FastAPI app: {e}")
        raise

def main():
    """Run the server"""
    try:
        print("🔧 Creating FastAPI app...")
        app = create_simple_app()
        print("✅ FastAPI app created successfully!")
        
        import uvicorn
        print("✅ Uvicorn imported successfully!")
        
        port = int(os.environ.get("PORT", 8000))
        host = "0.0.0.0"
        
        print(f"🚀 Starting server on http://{host}:{port}")
        print("📚 Test endpoints:")
        print(f"   - Root: http://localhost:{port}/")
        print(f"   - Health: http://localhost:{port}/health")
        print(f"   - Test: http://localhost:{port}/test")
        print("=" * 50)
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
