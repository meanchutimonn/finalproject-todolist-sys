from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from datetime import datetime

# FastAPI App
app = FastAPI(title="To-Do List API", description="Manage users and tasks")

# Database Configuration
DB_CONFIG = {
    "host": "192.168.100.23",
    "user": "root",  # Change this to your database user
    "password": "P@ssw0rd",  # Change this to your database password
    "database": "to_do_list"
}

# ==================== PYDANTIC MODELS ====================

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    email: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[int] = None

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[int] = None    # แก้ไขจาก str เป็น int ตาม DB
    deadline: Optional[datetime] = None # แก้ไขจาก str เป็น datetime ตาม DB
    status: str = "pending"
    friend_assignid: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    task_id: int

    class Config:
        from_attributes = True

# ==================== DB CONNECTION ====================

@contextmanager
def get_db_connection():
    """Create and manage database connection"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if connection and connection.is_connected():
            connection.close()

# ==================== USER ENDPOINTS ====================

@app.get("/")
def home():
    return {"message": "Welcome to the To-Do List API!"}

@app.post("/user_login", response_model=LoginResponse)
def user_login(login_request: LoginRequest):
    """Login user by username and email verification"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, username, email FROM user WHERE username = %s AND email = %s",
                (login_request.username, login_request.email)
            )
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                return {
                    "success": True,
                    "message": "Login successful",
                    "user_id": user["id"]
                }
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid username or email"
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login error: {str(e)}"
        )

@app.get("/users", response_model=List[User])
def get_all_users():
    """Get all users"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, email FROM user")
            users = cursor.fetchall()
            cursor.close()
            return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int):
    """Get a specific user by ID"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, email FROM user WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create a new user"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO user (username, email) VALUES (%s, %s)",
                (user.username, user.email)
            )
            connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

# ==================== TASK ENDPOINTS ====================

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """Get all tasks"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT task_id, title, description, priority, deadline, status, friend_assignid FROM task")
            tasks = cursor.fetchall()
            cursor.close()
            return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: int):
    """Get a specific task by ID"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT task_id, title, description, priority, deadline, status, friend_assignid FROM task WHERE task_id = %s", (task_id,))
            task = cursor.fetchone()
            cursor.close()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task: {str(e)}")

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """Create a new task"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO task (title, description, priority, deadline, status, friend_assignid) VALUES (%s, %s, %s, %s, %s, %s)",
                (task.title, task.description, task.priority, task.deadline, task.status, task.friend_assignid)
            )
            connection.commit()
            task_id = cursor.lastrowid
            cursor.close()
            return {**task.dict(), "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    """Update an existing task"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT task_id FROM task WHERE task_id = %s", (task_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Task not found")
            
            cursor.execute(
                "UPDATE task SET title = %s, description = %s, priority = %s, deadline = %s, status = %s, friend_assignid = %s WHERE task_id = %s",
                (task.title, task.description, task.priority, task.deadline, task.status, task.friend_assignid, task_id)
            )
            connection.commit()
            cursor.close()
            return {**task.dict(), "task_id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Delete a task"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT task_id FROM task WHERE task_id = %s", (task_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Task not found")
            
            cursor.execute("DELETE FROM task WHERE task_id = %s", (task_id,))
            connection.commit()
            cursor.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_user_tasks(user_id: int):
    """Get all tasks assigned to a specific user (friend_assignid)"""
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT task_id, title, description, priority, deadline, status, friend_assignid FROM task WHERE friend_assignid = %s", (user_id,))
            tasks = cursor.fetchall()
            cursor.close()
            
            if not tasks:
                return []
                
            return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user tasks: {str(e)}")