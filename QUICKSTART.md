# 🚀 Quick Start Guide

## Step 1: Prepare Database Configuration

Before starting, make sure you have:
- MariaDB/MySQL running on `192.168.100.23`
- A database named `to_do_list`
- Valid database username/password

## Step 2: Setup Python Environment

### Option A: Using Virtual Environment (Recommended)
```bash
# List existing environment
dir env

# Activate the virtual environment
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Using System Python
```bash
pip install -r requirements.txt
```

## Step 3: Create Database Tables

Run the setup script to automatically create the database and tables:

```bash
python setup_database.py
```

This will create:
- `user` table (for storing user information)
- `task` table (for storing tasks)

## Step 4: Update Database Credentials (Optional)

You can configure credentials in two ways:

**Option A: Direct Configuration**
Edit `to_do_list.py` and update:
```python
DB_CONFIG = {
    "host": "192.168.100.23",
    "user": "your_db_user",      # Change this
    "password": "your_password",  # Change this
    "database": "to_do_list"
}
```

**Option B: Environment Variables (Recommended)**
1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```
   DB_HOST=192.168.100.23
   DB_USER=your_db_user
   DB_PASSWORD=your_password
   DB_NAME=to_do_list
   ```

3. The `config.py` will automatically load these values

## Step 5: Start the API Server

```bash
# Using the default port (8000)
uvicorn to_do_list:app --reload

# OR specify custom host and port
uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
```

## Step 6: Access the API

### Swagger UI (Interactive Documentation)
```
http://localhost:8000/docs
```

### ReDoc (Alternative Documentation)
```
http://localhost:8000/redoc
```

### Test the API
```bash
# Using the test script
python test_api.py

# Or manually test with cURL
curl http://localhost:8000/
```

---

## 📊 Available API Endpoints

### Users
- `GET /users` - Get all users
- `GET /users/{id}` - Get specific user
- `POST /users` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Tasks
- `GET /tasks` - Get all tasks
- `GET /tasks/{id}` - Get specific task
- `POST /tasks` - Create task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Bonus
- `GET /users/{id}/tasks` - Get all tasks for specific user

---

## ✅ Verification Checklist

After setup, verify everything is working:

- [ ] Database created successfully
- [ ] Tables created (user, task)
- [ ] API server running (no errors)
- [ ] Can access http://localhost:8000/docs
- [ ] `/` endpoint returns welcome message
- [ ] Database connection works

---

## 🐛 Troubleshooting

### 1. Database Connection Error
```
Error: Can't connect to MySQL server on '192.168.100.23'
```
**Solution:**
- Check if MariaDB is running
- Verify IP address is correct
- Check username/password
- Check firewall settings

### 2. Table Not Found Error
```
Error: Table 'to_do_list.user' doesn't exist
```
**Solution:**
```bash
python setup_database.py
```

### 3. Port Already in Use
```
OSError: [Errno 10048] Only one usage of each socket address is normally permitted
```
**Solution:**
```bash
# Use a different port
uvicorn to_do_list:app --port 8001
```

### 4. Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### 5. Permission Denied Error
**Solution:** Make sure your database user has necessary permissions

---

## 📝 Example Requests

### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"john_doe\",
    \"email\": \"john@example.com\",
    \"password\": \"securepass123\"
  }"
```

### Get All Tasks
```bash
curl -X GET "http://localhost:8000/tasks"
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"My First Task\",
    \"description\": \"Complete the project\",
    \"user_id\": 1,
    \"status\": \"pending\"
  }"
```

---

## 💡 Next Steps

1. Access Swagger UI at http://localhost:8000/docs
2. Test endpoints interactively
3. Review README.md for detailed API documentation
4. Customize the API for your needs

Enjoy your To-Do List API! 🎉
