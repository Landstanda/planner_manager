#!/usr/bin/env python3
"""
Test script to verify Python service foundation setup.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_imports():
    """Test that all our core modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test core imports
        from app.core.config import settings
        print("✅ Core config imported successfully")
        
        from app.models.database import Task, Project
        print("✅ Database models imported successfully")
        
        from app.schemas.task import TaskCreate, TaskResponse
        print("✅ Pydantic schemas imported successfully")
        
        from app.services.ai_service import AIService
        print("✅ AI service imported successfully")
        
        from app.services.task_service import TaskService
        print("✅ Task service imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    try:
        from app.core.config import settings
        
        print("\nTesting configuration...")
        print(f"App name: {settings.app_name}")
        print(f"App version: {settings.app_version}")
        print(f"Debug mode: {settings.debug}")
        print(f"API path: {settings.api_v1_str}")
        
        # Test required fields exist (even if not set)
        assert hasattr(settings, 'supabase_url')
        assert hasattr(settings, 'openai_api_key')
        assert hasattr(settings, 'secret_key')
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_pydantic_schemas():
    """Test Pydantic schema validation."""
    try:
        from app.schemas.task import TaskCreate, TaskUpdate
        
        print("\nTesting Pydantic schemas...")
        
        # Test valid task creation
        task_data = TaskCreate(
            title="Test Task",
            description="A test task",
            priority=2,
            est_duration=30
        )
        
        print(f"Created task schema: {task_data.title}")
        
        # Test validation
        try:
            invalid_task = TaskCreate(
                title="",  # This should fail validation
                priority=10  # This should also fail (out of range)
            )
            print("❌ Validation should have failed")
            return False
        except Exception:
            print("✅ Validation working correctly")
        
        print("✅ Pydantic schemas working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Schema error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Python Service Foundation Setup\n")
    
    tests = [
        test_imports,
        test_config,
        test_pydantic_schemas
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    if all(results):
        print("🎉 ALL TESTS PASSED! Python service foundation is ready.")
        print("\nNext steps:")
        print("1. Set up environment variables (.env file)")
        print("2. Create API endpoints")
        print("3. Test with real database connection")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 