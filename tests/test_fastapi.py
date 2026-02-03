"""
Test script for FastAPI endpoints
Run this after starting the FastAPI server to verify all endpoints work
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📦 Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_query():
    """Test query endpoint"""
    print("\n🔍 Testing Query Endpoint...")
    try:
        payload = {
            "question": "Show all tables in the database",
            "chat_history": []
        }
        response = requests.post(
            f"{BASE_URL}/api/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status Code: {response.status_code}")
        print(f"📦 Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_docs():
    """Test documentation endpoints"""
    print("\n🔍 Testing Documentation Endpoints...")
    try:
        # Test Swagger UI
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ Swagger UI (/docs): {response.status_code}")
        
        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc")
        print(f"✅ ReDoc (/redoc): {response.status_code}")
        
        # Test OpenAPI schema
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"✅ OpenAPI Schema (/openapi.json): {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 FastAPI Endpoint Testing")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    results = []
    
    # Test health endpoint
    results.append(("Health", test_health()))
    
    # Test query endpoint
    results.append(("Query", test_query()))
    
    # Test documentation endpoints
    results.append(("Documentation", test_docs()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! FastAPI server is working correctly.")
        print("\n🌐 Visit these URLs:")
        print(f"   • API Docs: {BASE_URL}/docs")
        print(f"   • ReDoc: {BASE_URL}/redoc")
        print(f"   • Health: {BASE_URL}/api/health")
    else:
        print("⚠️  Some tests failed. Check if the server is running.")
        print(f"   Run: python api_server_simple_fastapi.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
