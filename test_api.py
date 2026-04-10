"""
Test Script for To-Do List API
This script tests all API endpoints
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_result(test_name: str, success: bool, response: Any = None):
    """Print test result"""
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if success else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {test_name}")
    if response and not success:
        print(f"  Response: {response}")

def test_api():
    """Test all API endpoints"""
    print(f"{Colors.BLUE}=== To-Do List API Tests ==={Colors.END}\n")
    
    user_id = None
    task_id = None
    
    try:
        # Test 1: Get home
        print(f"{Colors.YELLOW}1. Testing Home Endpoint{Colors.END}")
        response = requests.get(f"{BASE_URL}/")
        print_result("GET /", response.status_code == 200, response.json())
        print()
        
        # Test 2: Create User
        print(f"{Colors.YELLOW}2. Testing User Creation{Colors.END}")
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        success = response.status_code == 201
        print_result("POST /users", success, response.json())
        if success:
            user_id = response.json()["id"]
            print(f"  Created User ID: {user_id}")
        print()
        
        # Test 3: Get All Users
        print(f"{Colors.YELLOW}3. Testing Get All Users{Colors.END}")
        response = requests.get(f"{BASE_URL}/users")
        success = response.status_code == 200 and isinstance(response.json(), list)
        print_result("GET /users", success, response.json())
        print()
        
        # Test 4: Get User by ID
        if user_id:
            print(f"{Colors.YELLOW}4. Testing Get User by ID{Colors.END}")
            response = requests.get(f"{BASE_URL}/users/{user_id}")
            success = response.status_code == 200
            print_result(f"GET /users/{user_id}", success, response.json())
            print()
        
        # Test 5: Update User
        if user_id:
            print(f"{Colors.YELLOW}5. Testing Update User{Colors.END}")
            updated_user = {
                "username": "testuser_updated",
                "email": "updated@example.com",
                "password": "newpass123"
            }
            response = requests.put(f"{BASE_URL}/users/{user_id}", json=updated_user)
            success = response.status_code == 200
            print_result(f"PUT /users/{user_id}", success, response.json())
            print()
        
        # Test 6: Create Task
        if user_id:
            print(f"{Colors.YELLOW}6. Testing Task Creation{Colors.END}")
            task_data = {
                "title": "Test Task",
                "description": "This is a test task",
                "user_id": user_id,
                "status": "pending"
            }
            response = requests.post(f"{BASE_URL}/tasks", json=task_data)
            success = response.status_code == 201
            print_result("POST /tasks", success, response.json())
            if success:
                task_id = response.json()["id"]
                print(f"  Created Task ID: {task_id}")
            print()
        
        # Test 7: Get All Tasks
        print(f"{Colors.YELLOW}7. Testing Get All Tasks{Colors.END}")
        response = requests.get(f"{BASE_URL}/tasks")
        success = response.status_code == 200 and isinstance(response.json(), list)
        print_result("GET /tasks", success, response.json())
        print()
        
        # Test 8: Get Task by ID
        if task_id:
            print(f"{Colors.YELLOW}8. Testing Get Task by ID{Colors.END}")
            response = requests.get(f"{BASE_URL}/tasks/{task_id}")
            success = response.status_code == 200
            print_result(f"GET /tasks/{task_id}", success, response.json())
            print()
        
        # Test 9: Update Task
        if task_id:
            print(f"{Colors.YELLOW}9. Testing Update Task{Colors.END}")
            updated_task = {
                "title": "Updated Test Task",
                "description": "Updated description",
                "user_id": user_id,
                "status": "in_progress"
            }
            response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_task)
            success = response.status_code == 200
            print_result(f"PUT /tasks/{task_id}", success, response.json())
            print()
        
        # Test 10: Get User Tasks
        if user_id:
            print(f"{Colors.YELLOW}10. Testing Get User Tasks{Colors.END}")
            response = requests.get(f"{BASE_URL}/users/{user_id}/tasks")
            success = response.status_code == 200 and isinstance(response.json(), list)
            print_result(f"GET /users/{user_id}/tasks", success, response.json())
            print()
        
        # Test 11: Delete Task
        if task_id:
            print(f"{Colors.YELLOW}11. Testing Delete Task{Colors.END}")
            response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
            success = response.status_code == 204
            print_result(f"DELETE /tasks/{task_id}", success)
            print()
        
        # Test 12: Delete User
        if user_id:
            print(f"{Colors.YELLOW}12. Testing Delete User{Colors.END}")
            response = requests.delete(f"{BASE_URL}/users/{user_id}")
            success = response.status_code == 204
            print_result(f"DELETE /users/{user_id}", success)
            print()
        
        print(f"{Colors.BLUE}=== Tests Complete ==={Colors.END}")
        
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}✗ Error: Cannot connect to API at {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Make sure the API is running:{Colors.END}")
        print(f"  uvicorn to_do_list:app --reload\n")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {str(e)}{Colors.END}")

if __name__ == "__main__":
    test_api()
