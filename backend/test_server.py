#!/usr/bin/env python3
"""
Test server to verify FastAPI is working
"""

import uvicorn
from fastapi import FastAPI

# Create a simple test app
app = FastAPI(
    title="Test Medicine Delivery API",
    description="Test server to verify FastAPI is working",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Test server is running!", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "test-api"}

@app.get("/test")
async def test():
    return {"message": "All systems working!", "python_version": "3.13.3"}

if __name__ == "__main__":
    print("🚀 Starting test server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
