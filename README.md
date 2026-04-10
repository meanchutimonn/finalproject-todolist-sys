# To-Do List API

A comprehensive REST API built with FastAPI for managing users and tasks, connected to a MariaDB database.

## 📋 Prerequisites

- Python 3.8+
- MariaDB/MySQL Server
- Database: `to_do_list`
- Host: `192.168.100.23`

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

Edit `to_do_list.py` and update the `DB_CONFIG` with your database credentials:

```python
DB_CONFIG = {
    "host": "192.168.100.23",
    "user": "root",          # Change your username
    "password": "",          # Change your password
    "database": "to_do_list"
}
```

### 3. Create Database Tables

Run the setup script to create the necessary tables:

```bash
python setup_database.py
```

### 4. Start the API Server

```bash
uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 API Endpoints

### **USER ENDPOINTS**

#### 1. Get All Users
```
GET /users
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "password": "hashed_password"
  }
]
```

#### 2. Get User by ID
```
GET /users/{user_id}
```

**Parameters:**
- `user_id` (int): User ID

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "password": "hashed_password"
}
```

#### 3. Create User
```
POST /users
```

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### 4. Update User
```
PUT /users/{user_id}
```

**Parameters:**
- `user_id` (int): User ID

**Request Body:**
```json
{
  "username": "john_doe_updated",
  "email": "john_new@example.com",
  "password": "newpassword"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe_updated",
  "email": "john_new@example.com",
  "password": "newpassword"
}
```

#### 5. Delete User
```
DELETE /users/{user_id}
```

**Parameters:**
- `user_id` (int): User ID

**Response:** (204 No Content)

---

### **TASK ENDPOINTS**

#### 1. Get All Tasks
```
GET /tasks
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the API documentation",
    "user_id": 1,
    "status": "in_progress"
  }
]
```

#### 2. Get Task by ID
```
GET /tasks/{task_id}
```

**Parameters:**
- `task_id` (int): Task ID

**Response:**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the API documentation",
  "user_id": 1,
  "status": "in_progress"
}
```

#### 3. Create Task
```
POST /tasks
```

**Request Body:**
```json
{
  "title": "Complete project",
  "description": "Finish the API documentation",
  "user_id": 1,
  "status": "pending"
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the API documentation",
  "user_id": 1,
  "status": "pending"
}
```

#### 4. Update Task
```
PUT /tasks/{task_id}
```

**Parameters:**
- `task_id` (int): Task ID

**Request Body:**
```json
{
  "title": "Complete project",
  "description": "Finish the API documentation",
  "user_id": 1,
  "status": "completed"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the API documentation",
  "user_id": 1,
  "status": "completed"
}
```

#### 5. Delete Task
```
DELETE /tasks/{task_id}
```

**Parameters:**
- `task_id` (int): Task ID

**Response:** (204 No Content)

---

### **BONUS ENDPOINT**

#### Get All Tasks for a Specific User
```
GET /users/{user_id}/tasks
```

**Parameters:**
- `user_id` (int): User ID

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the API documentation",
    "user_id": 1,
    "status": "in_progress"
  },
  {
    "id": 2,
    "title": "Review code",
    "description": "Review pull requests",
    "user_id": 1,
    "status": "pending"
  }
]
```

---

## 🗄️ Database Schema

### **user table**
| Column      | Type         | Constraints          |
|-------------|--------------|----------------------|
| id          | INT          | PRIMARY KEY, AUTO_INCREMENT |
| username    | VARCHAR(100) | NOT NULL, UNIQUE     |
| email       | VARCHAR(100) | NOT NULL, UNIQUE     |
| password    | VARCHAR(255) | NOT NULL             |
| created_at  | TIMESTAMP    | DEFAULT NOW()        |

### **task table**
| Column      | Type         | Constraints                        |
|-------------|--------------|-----------------------------------|
| id          | INT          | PRIMARY KEY, AUTO_INCREMENT       |
| title       | VARCHAR(255) | NOT NULL                          |
| description | TEXT         | NULL                              |
| user_id     | INT          | NOT NULL, FOREIGN KEY (user.id)   |
| status      | ENUM         | pending, in_progress, completed   |
| created_at  | TIMESTAMP    | DEFAULT NOW()                     |
| updated_at  | TIMESTAMP    | DEFAULT NOW(), UPDATE CURRENT_TIMESTAMP |

---

## 🔒 Security Notes

⚠️ **Important Security Recommendations:**

1. **Password Hashing**: Consider using `bcrypt` or `argon2` to hash passwords before storing
2. **Environment Variables**: Move database credentials to `.env` file using `python-dotenv`
3. **Authentication**: Implement JWT tokens for API authentication
4. **HTTPS**: Use HTTPS in production
5. **CORS**: Configure CORS appropriately for your frontend

---

## 🛠️ Example Usage

### Using cURL

```bash
# Create a user
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'

# Get all tasks
curl -X GET "http://localhost:8000/tasks"

# Get user by ID
curl -X GET "http://localhost:8000/users/1"

# Create a task
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task","description":"Task details","user_id":1,"status":"pending"}'

# Update a task
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Task Updated","description":"Updated details","user_id":1,"status":"completed"}'

# Delete a task
curl -X DELETE "http://localhost:8000/tasks/1"
```

### Using Python (requests library)

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a user
user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass"
}
response = requests.post(f"{BASE_URL}/users", json=user_data)
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())

# Get user by ID
response = requests.get(f"{BASE_URL}/users/1")
print(response.json())
```

---

## 📝 Status Codes

| Code | Meaning                  |
|------|--------------------------|
| 200  | OK - Request succeeded   |
| 201  | Created - New resource created |
| 204  | No Content - Deletion successful |
| 400  | Bad Request - Invalid input |
| 404  | Not Found - Resource not found |
| 500  | Server Error - Internal error |

---

## 🐛 Troubleshooting

### Connection Error
- Verify MariaDB server is running
- Check host, user, and password in `DB_CONFIG`
- Ensure database `to_do_list` exists

### Table Not Found
- Run `python setup_database.py` to create tables

### Port Already in Use
- Use different port: `uvicorn to_do_list:app --port 8001`

---

## 📦 Project Structure

```
to_dolist/
├── to_do_list.py           # Main API file
├── setup_database.py       # Database initialization script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 📄 License

This project is open source and available under the MIT License.

---

## 💡 Author Notes

Created with FastAPI for building modern, fast Python APIs with automatic interactive documentation.
