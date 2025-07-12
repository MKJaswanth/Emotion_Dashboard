#!/usr/bin/env python3
"""
Test script for Emotion Analytics API
Run this to verify all endpoints are working correctly
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_api_info():
    """Test API info endpoint"""
    print("\n🔍 Testing API info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/test")
        if response.status_code == 200:
            print("✅ API info endpoint working")
            data = response.json()
            print(f"   Message: {data['message']}")
            print(f"   JWT Available: {data['jwt_available']}")
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info error: {e}")
        return False

def test_nlp():
    """Test NLP functionality"""
    print("\n🔍 Testing NLP functionality...")
    try:
        response = requests.get(f"{BASE_URL}/test-nlp")
        if response.status_code == 200:
            print("✅ NLP test passed")
            data = response.json()
            print(f"   Sample text: {data['sample_text']}")
            print(f"   Sentiment: {data['analysis']['sentiment']['category']}")
            return True
        else:
            print(f"❌ NLP test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ NLP test error: {e}")
        return False

def test_auth_register():
    """Test user registration"""
    print("\n🔍 Testing user registration...")
    try:
        data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        if response.status_code == 201:
            print("✅ Registration successful")
            data = response.json()
            print(f"   User ID: {data['user']['id']}")
            print(f"   Token received: {'Yes' if data['token'] else 'No'}")
            return data['token']
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_auth_login():
    """Test user login"""
    print("\n🔍 Testing user login...")
    try:
        data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        if response.status_code == 200:
            print("✅ Login successful")
            data = response.json()
            print(f"   User: {data['user']['name']}")
            print(f"   Token received: {'Yes' if data['token'] else 'No'}")
            return data['token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_mood_submit(token):
    """Test mood submission with authentication"""
    print("\n🔍 Testing mood submission...")
    if not token:
        print("❌ No token available for mood submission")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "mood_score": 4,
            "text": "I'm feeling great today! The team is working well together.",
            "activity": "team_meeting"
        }
        response = requests.post(f"{BASE_URL}/api/mood/submit", json=data, headers=headers)
        if response.status_code == 201:
            print("✅ Mood submission successful")
            data = response.json()
            print(f"   Mood score: {data['mood_entry']['mood_score']}")
            print(f"   Analysis available: {'Yes' if data['analysis'] else 'No'}")
            return True
        else:
            print(f"❌ Mood submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Mood submission error: {e}")
        return False

def test_text_analysis():
    """Test text analysis endpoint"""
    print("\n🔍 Testing text analysis...")
    try:
        data = {
            "text": "I'm feeling stressed about the upcoming deadline but excited about the project potential."
        }
        response = requests.post(f"{BASE_URL}/analyze-text", json=data)
        if response.status_code == 200:
            print("✅ Text analysis successful")
            data = response.json()
            print(f"   Sentiment: {data['analysis']['sentiment']['category']}")
            print(f"   Primary emotion: {data['analysis']['emotions']['primary_emotion']}")
            return True
        else:
            print(f"❌ Text analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Text analysis error: {e}")
        return False

def test_team_analytics():
    """Test team analytics endpoint"""
    print("\n🔍 Testing team analytics...")
    try:
        response = requests.get(f"{BASE_URL}/analyze-team/all")
        if response.status_code == 200:
            print("✅ Team analytics successful")
            data = response.json()
            print(f"   Team: {data['team_name']}")
            print(f"   Analysis available: {'Yes' if data['analysis'] else 'No'}")
            return True
        else:
            print(f"❌ Team analytics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Team analytics error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Emotion Analytics API Tests")
    print("=" * 50)
    
    # Check if server is running
    if not test_health():
        print("\n❌ Server is not running. Please start the server first:")
        print("   cd backend")
        print("   python app.py")
        sys.exit(1)
    
    # Run all tests
    tests = [
        test_api_info,
        test_nlp,
        test_auth_register,
        test_auth_login,
        test_text_analysis,
        test_team_analytics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    # Test mood submission with token
    token = test_auth_login()
    if token and test_mood_submit(token):
        passed += 1
    total += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n🔗 API Endpoints available:")
    print("   - Health: GET /health")
    print("   - API Info: GET /api/test")
    print("   - Register: POST /api/auth/register")
    print("   - Login: POST /api/auth/login")
    print("   - Submit Mood: POST /api/mood/submit")
    print("   - Text Analysis: POST /analyze-text")
    print("   - Team Analytics: GET /analyze-team/<team>")

if __name__ == "__main__":
    main() 