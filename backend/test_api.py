"""
Comprehensive API testing script for Quick Commerce Medicine Delivery Application
"""

import requests
import json
from datetime import date, datetime
import time

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
        
    def test_health_check(self):
        """Test health check endpoint"""
        print("🔍 Testing Health Check...")
        response = self.session.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        print("✅ Health check passed")
        
    def test_user_registration(self):
        """Test user registration"""
        print("🔍 Testing User Registration...")
        user_data = {
            "email": "testuser@example.com",
            "phone": "+919876543210",
            "password": "Test@123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = self.session.post(f"{API_BASE}/auth/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        self.auth_token = data["access_token"]
        self.user_id = data["user"]["id"]
        
        # Set authorization header for future requests
        self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
        print("✅ User registration passed")
        
    def test_user_login(self):
        """Test user login"""
        print("🔍 Testing User Login...")
        login_data = {
            "email": "testuser@example.com",
            "password": "Test@123"
        }
        
        response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        print("✅ User login passed")
        
    def test_get_current_user(self):
        """Test get current user profile"""
        print("🔍 Testing Get Current User...")
        response = self.session.get(f"{API_BASE}/auth/me")
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == "testuser@example.com"
        print("✅ Get current user passed")
        
    def test_categories(self):
        """Test category endpoints"""
        print("🔍 Testing Categories...")
        
        # Get all categories
        response = self.session.get(f"{API_BASE}/categories/")
        assert response.status_code == 200
        
        categories = response.json()
        assert len(categories) > 0
        print(f"✅ Found {len(categories)} categories")
        
        # Get categories with counts
        response = self.session.get(f"{API_BASE}/categories/with-counts")
        assert response.status_code == 200
        print("✅ Categories with counts passed")
        
    def test_medicines(self):
        """Test medicine endpoints"""
        print("🔍 Testing Medicines...")
        
        # Search all medicines
        response = self.session.get(f"{API_BASE}/medicines/search")
        assert response.status_code == 200
        
        data = response.json()
        assert "medicines" in data
        assert data["total"] > 0
        print(f"✅ Found {data['total']} medicines")
        
        # Search with query
        response = self.session.get(f"{API_BASE}/medicines/search?q=paracetamol")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["medicines"]) > 0
        print("✅ Medicine search with query passed")
        
        # Search prescription medicines
        response = self.session.get(f"{API_BASE}/medicines/search?prescription_required=true")
        assert response.status_code == 200
        
        data = response.json()
        print(f"✅ Found {data['total']} prescription medicines")
        
        return data["medicines"][0]["id"] if data["medicines"] else None
        
    def test_cart_operations(self, medicine_id):
        """Test cart operations"""
        if not medicine_id:
            print("⚠️ Skipping cart tests - no medicine ID available")
            return
            
        print("🔍 Testing Cart Operations...")
        
        # Get empty cart
        response = self.session.get(f"{API_BASE}/cart/")
        assert response.status_code == 200
        
        cart = response.json()
        assert cart["total_items"] == 0
        print("✅ Empty cart retrieved")
        
        # Add item to cart
        add_item_data = {
            "medicine_id": medicine_id,
            "quantity": 2,
            "notes": "Test order"
        }
        
        response = self.session.post(f"{API_BASE}/cart/items", json=add_item_data)
        assert response.status_code == 201
        
        item = response.json()
        assert item["quantity"] == 2
        print("✅ Item added to cart")
        
        # Get cart with items
        response = self.session.get(f"{API_BASE}/cart/")
        assert response.status_code == 200
        
        cart = response.json()
        assert cart["total_items"] == 1
        assert cart["subtotal"] > 0
        print("✅ Cart with items retrieved")
        
        # Get cart summary
        response = self.session.get(f"{API_BASE}/cart/summary")
        assert response.status_code == 200
        
        summary = response.json()
        assert summary["total_items"] == 1
        print("✅ Cart summary retrieved")
        
        return cart["items"][0]["id"]
        
    def test_order_creation(self):
        """Test order creation from cart"""
        print("🔍 Testing Order Creation...")
        
        order_data = {
            "delivery_address": {
                "street": "123 Test Street",
                "city": "Mumbai",
                "state": "Maharashtra",
                "postal_code": "400001",
                "country": "India",
                "contact_phone": "+919876543210",
                "contact_name": "Test User"
            },
            "payment_method": "cash_on_delivery",
            "delivery_instructions": "Ring the bell twice",
            "validate_prescriptions": False
        }
        
        response = self.session.post(f"{API_BASE}/orders/from-cart", json=order_data)
        assert response.status_code == 201
        
        order = response.json()
        assert order["status"] == "pending"
        assert len(order["items"]) > 0
        print("✅ Order created from cart")
        
        return order["id"]
        
    def test_order_operations(self, order_id):
        """Test order operations"""
        if not order_id:
            print("⚠️ Skipping order operations - no order ID available")
            return
            
        print("🔍 Testing Order Operations...")
        
        # Get order by ID
        response = self.session.get(f"{API_BASE}/orders/{order_id}")
        assert response.status_code == 200
        
        order = response.json()
        assert order["id"] == order_id
        print("✅ Order retrieved by ID")
        
        # Get user orders
        response = self.session.get(f"{API_BASE}/orders/")
        assert response.status_code == 200
        
        orders = response.json()
        assert len(orders) > 0
        print("✅ User orders retrieved")
        
        # Get order tracking
        response = self.session.get(f"{API_BASE}/orders/{order_id}/tracking")
        assert response.status_code == 200
        
        tracking = response.json()
        assert tracking["order_id"] == order_id
        print("✅ Order tracking retrieved")
        
    def test_prescription_stats(self):
        """Test prescription statistics"""
        print("🔍 Testing Prescription Stats...")
        
        response = self.session.get(f"{API_BASE}/prescriptions/stats/overview")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_prescriptions" in stats
        print("✅ Prescription stats retrieved")
        
    def test_order_stats(self):
        """Test order statistics"""
        print("🔍 Testing Order Stats...")
        
        response = self.session.get(f"{API_BASE}/orders/stats/overview")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_orders" in stats
        print("✅ Order stats retrieved")
        
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Comprehensive API Tests...\n")
        
        try:
            # Basic tests
            self.test_health_check()
            self.test_user_registration()
            self.test_user_login()
            self.test_get_current_user()
            
            # Catalog tests
            self.test_categories()
            medicine_id = self.test_medicines()
            
            # Cart and order tests
            cart_item_id = self.test_cart_operations(medicine_id)
            order_id = self.test_order_creation()
            self.test_order_operations(order_id)
            
            # Statistics tests
            self.test_prescription_stats()
            self.test_order_stats()
            
            print("\n🎉 All API tests passed successfully!")
            print("✅ Backend implementation is working correctly!")
            
        except AssertionError as e:
            print(f"\n❌ Test failed: {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Request failed: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False
            
        return True


if __name__ == "__main__":
    print("Quick Commerce Medicine Delivery API - Comprehensive Test Suite")
    print("=" * 60)
    
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 Backend implementation is complete and functional!")
    else:
        print("\n⚠️ Some tests failed. Please check the server logs.")
