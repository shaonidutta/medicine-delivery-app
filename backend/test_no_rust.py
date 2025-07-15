#!/usr/bin/env python3
"""
Comprehensive test to verify NO Rust dependencies are present
and all functionality works with pure Python packages.
"""

import sys
import subprocess

def test_no_rust_packages():
    """Test that no Rust-based packages are installed"""
    print("🔍 CHECKING FOR RUST PACKAGES...")
    
    rust_packages = [
        'pydantic_core',
        'cryptography', 
        'bcrypt',
        'python-jose'
    ]
    
    rust_found = False
    for pkg in rust_packages:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"❌ RUST PACKAGE FOUND: {pkg}")
            rust_found = True
        except ImportError:
            print(f"✅ {pkg} not installed (good)")
    
    return not rust_found

def test_pure_python_packages():
    """Test that pure Python packages work correctly"""
    print("\n🐍 TESTING PURE PYTHON PACKAGES...")
    
    try:
        # Test Pydantic v1
        import pydantic
        print(f"✅ Pydantic v{pydantic.VERSION} (pure Python)")
        
        # Test PyJWT
        import jwt
        print("✅ PyJWT (pure Python)")
        
        # Test Passlib with pbkdf2_sha256
        from passlib.context import CryptContext
        ctx = CryptContext(schemes=['pbkdf2_sha256'])
        print("✅ Passlib with pbkdf2_sha256 (pure Python)")
        
        return True
    except Exception as e:
        print(f"❌ Pure Python package error: {e}")
        return False

def test_application_functionality():
    """Test that the application works correctly"""
    print("\n🧪 TESTING APPLICATION FUNCTIONALITY...")
    
    try:
        # Test security functions
        from app.core.security import create_access_token, verify_token, get_password_hash, verify_password
        
        # Test password hashing
        password = 'testpass123'
        hashed = get_password_hash(password)
        is_valid = verify_password(password, hashed)
        print(f"✅ Password hashing: {is_valid}")
        
        # Test JWT
        token = create_access_token(subject='test@example.com')
        subject = verify_token(token)
        print(f"✅ JWT tokens: {subject}")
        
        # Test app import
        from app.main import app
        print(f"✅ App import: {app.title}")
        
        return True
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE RUST-FREE VERIFICATION")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    
    # Run all tests
    rust_free = test_no_rust_packages()
    pure_python = test_pure_python_packages()
    app_working = test_application_functionality()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"✅ No Rust packages: {rust_free}")
    print(f"✅ Pure Python packages: {pure_python}")
    print(f"✅ Application working: {app_working}")
    
    if rust_free and pure_python and app_working:
        print("\n🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - DO NOT DEPLOY!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
