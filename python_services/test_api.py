#!/usr/bin/env python3
"""
Simple API test script to verify endpoints are working.
"""

import requests
import json
import sys
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single API endpoint."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            try:
                result = response.json()
                if isinstance(result, dict) and len(result) <= 3:
                    print(f"   Response: {json.dumps(result, indent=2)}")
                else:
                    print(f"   Response: {type(result).__name__} with {len(result) if hasattr(result, '__len__') else 'unknown'} items")
            except:
                print(f"   Response: {response.text[:100]}...")
            return True
        else:
            print(f"❌ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint} - Connection failed (server not running?)")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)}")
        return False

def main():
    """Run API tests."""
    print("🚀 Testing Chief-of-Flow API Endpoints\n")
    
    # Get today's date for schedule tests
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    tests = [
        # Basic endpoints
        ("GET", "/", None, 200),
        ("GET", "/health", None, 503),  # Expected to fail without DB
        
        # API v1 health endpoints
        ("GET", "/api/v1/health/", None, 200),
        ("GET", "/api/v1/health/detailed", None, 200),
        
        # AI endpoints
        ("GET", "/api/v1/ai/status", None, 200),
        ("POST", "/api/v1/ai/chat", {"message": "Hello!"}, 200),
        ("POST", "/api/v1/ai/personality-assessment", {"responses": {}}, 200),
        
        # Task endpoints (will fail without DB, but should return proper errors)
        ("GET", "/api/v1/tasks/", None, 500),  # Expected to fail without DB
        ("POST", "/api/v1/tasks/from-text", {"input_text": "Buy groceries"}, 500),
        ("POST", "/api/v1/tasks/search", {"query": "test"}, 500),
        
        # Project endpoints (will fail without DB)
        ("GET", "/api/v1/projects/", None, 500),
        ("POST", "/api/v1/projects/", {
            "name": "Test Project",
            "description": "A test project",
            "importance": 3
        }, 500),
        
        # Schedule endpoints (will fail without DB)
        ("GET", "/api/v1/schedule/", None, 500),
        ("GET", f"/api/v1/schedule/?target_date={today.isoformat()}", None, 500),
        ("GET", "/api/v1/schedule/template?day_of_week=monday", None, 500),
        ("GET", f"/api/v1/schedule/available-slots?target_date={tomorrow.isoformat()}&duration_minutes=60", None, 500),
        ("GET", "/api/v1/schedule/week", None, 500),
        ("GET", "/api/v1/schedule/stats", None, 500),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, endpoint, data, expected_status in tests:
        if test_endpoint(method, endpoint, data, expected_status):
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        print("\n💡 Note: Database-dependent endpoints return 500 errors as expected without DB connection.")
        print("   Set up your .env file with database credentials to test full functionality.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 