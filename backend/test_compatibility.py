#!/usr/bin/env python3
"""
Test script to verify backend compatibility without running the full server
"""

def test_pydantic_imports():
    """Test Pydantic v1 imports"""
    try:
        import pydantic
        print(f"✅ Pydantic version: {pydantic.VERSION}")
        
        from pydantic import BaseModel, BaseSettings, validator
        print("✅ Pydantic imports successful!")
        
        # Test basic model
        class TestModel(BaseModel):
            name: str
            age: int
            
            @validator('age')
            @classmethod
            def validate_age(cls, v):
                if v < 0:
                    raise ValueError('Age must be positive')
                return v
        
        test_obj = TestModel(name="Test", age=25)
        print(f"✅ Pydantic model works: {test_obj.name}, {test_obj.age}")
        
        return True
    except Exception as e:
        print(f"❌ Pydantic error: {type(e).__name__}: {e}")
        return False

def test_config_import():
    """Test config import"""
    try:
        from app.core.config import settings
        print(f"✅ Config import successful!")
        print(f"   Project: {settings.PROJECT_NAME}")
        print(f"   API: {settings.API_V1_STR}")
        return True
    except Exception as e:
        print(f"❌ Config error: {type(e).__name__}: {e}")
        return False

def test_schema_imports():
    """Test schema imports"""
    try:
        from app.schemas.user import UserResponse
        from app.schemas.medicine import MedicineResponse
        from app.schemas.cart import CartResponse
        print("✅ Schema imports successful!")
        return True
    except Exception as e:
        print(f"❌ Schema error: {type(e).__name__}: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("🔧 Testing Backend Compatibility...")
    print("=" * 50)
    
    tests = [
        ("Pydantic Imports", test_pydantic_imports),
        ("Config Import", test_config_import),
        ("Schema Imports", test_schema_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All compatibility tests passed!")
        print("✅ Backend is ready for Python 3.11 deployment!")
    else:
        print("❌ Some tests failed - deployment may have issues")
    
    return passed == total

if __name__ == "__main__":
    main()
