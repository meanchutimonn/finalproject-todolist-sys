# 📱 To-Do List Project - Complete Overview

A full-stack To-Do List application featuring a **FastAPI REST API** backend and a beautiful **Flet mobile app** frontend.

## 📂 Project Structure

```
to_dolist/
├── to_do_list.py              # FastAPI REST API
├── mobile_app.py              # Flet Mobile Application
├── setup_database.py          # Database initialization
├── config.py                  # Configuration management
├── test_api.py               # API test suite
├── run.bat                   # Quick run script (Batch)
├── run.ps1                   # Quick run script (PowerShell)
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # API documentation
├── QUICKSTART.md            # Quick start guide
└── MOBILE_APP_GUIDE.md      # Mobile app documentation
```

## 🎯 Features

### Backend (FastAPI)
- ✅ RESTful API with all CRUD operations
- ✅ MariaDB database integration
- ✅ User management (GET, POST, PUT, DELETE)
- ✅ Task management (GET, POST, PUT, DELETE)
- ✅ Automatic API documentation (Swagger UI)
- ✅ Error handling and validation
- ✅ Database connection pooling

### Frontend (Flet Mobile App)
- ✅ Beautiful red and white UI design
- ✅ Single column responsive layout
- ✅ View all users and tasks
- ✅ Real-time data loading
- ✅ Auto-refresh functionality
- ✅ Error handling and status messages
- ✅ Works on Web, Desktop, iOS, and Android

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI 0.135.2 |
| Server | Uvicorn 0.42.0 |
| Database | MariaDB |
| ORM | mysql-connector-python |
| Frontend | Flet 0.83.1 |
| Validation | Pydantic 2.12.5 |
| HTTP Client | Requests 2.33.1 |
| Config | python-dotenv 1.2.2 |

## 📊 Database Schema

### User Table
```sql
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Task Table
```sql
CREATE TABLE task (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(50),
    deadline DATE,
    status VARCHAR(50) DEFAULT 'pending',
    friend_assignid INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (friend_assignid) REFERENCES user(id) ON DELETE SET NULL
);
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- MariaDB/MySQL 5.7+
- Windows, macOS, or Linux

### 2. Setup Database
```bash
# Activate virtual environment
env\Scripts\activate

# Run database setup script
python setup_database.py
```

### 3. Start API Server
```bash
env\Scripts\Activate.ps1
uvicorn to_do_list:app --reload --host 0.0.0.0 --port 8000
```

**API will be available at:**
- Home: http://localhost:8000/
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. Start Mobile App
```bash
env\Scripts\Activate.ps1
python mobile_app.py
```

**Mobile app will open in your web browser**

### One-Line Start (Both)
```bash
# Using PowerShell
./run.ps1
# Choose option 5 to run both API and Mobile

# Or Batch file
run.bat
# Choose option 5 to run both API and Mobile
```

## 📡 API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/users/{id}` | Get user by ID |
| POST | `/users` | Create new user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get task by ID |
| POST | `/tasks` | Create new task |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

### Bonus
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{user_id}/tasks` | Get tasks for user |

## 📱 Mobile App Features

### 👥 Users View
- Display all users
- Shows: ID, Username, Email
- Beautiful card layout
- Auto-refresh

### 📋 Tasks View
- Display all tasks
- Shows: Task ID, Title, Description, Priority, Deadline, Status, Assigned User
- Beautiful card layout
- Auto-refresh

### 🎨 UI Design
- **Background**: Bright Red (#CC0000)
- **Text**: White
- **Cards**: Dark Red (#990000)
- **Buttons**: Dark Red (#8B0000)
- **Layout**: Single column, scrollable

## 🔧 Configuration

### Environment Variables (.env)
```
DB_HOST=192.168.100.23
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=to_do_list
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### Mobile App API URL
Edit `mobile_app.py`:
```python
API_URL = "http://192.168.100.23:8000"
```

## 📖 Documentation

- **Main README**: [README.md](README.md) - API documentation
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Step-by-step setup
- **Mobile App**: [MOBILE_APP_GUIDE.md](MOBILE_APP_GUIDE.md) - Mobile app guide

## 🧪 Testing

### Test API Endpoints
```bash
python test_api.py
```

### Test Database Connection
```bash
python setup_database.py
```

### Manual API Testing
Access http://localhost:8000/docs for interactive API testing

## 💻 Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}'
```

### Get All Users
```bash
curl -X GET "http://localhost:8000/users"
```

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"My Task",
    "description":"Task details",
    "priority":"high",
    "deadline":"2024-12-31",
    "status":"pending",
    "friend_assignid":1
  }'
```

## 🐛 Troubleshooting

### API Not Starting
```
Error: Port 8000 already in use
```
**Solution:** Use different port:
```bash
uvicorn to_do_list:app --port 8001
```

### Database Connection Failed
```
Error: Can't connect to MySQL server
```
**Solution:**
1. Check if MariaDB is running
2. Verify connection settings in `.env`
3. Check firewall settings

### Mobile App Can't Connect to API
```
Failed to load users/tasks
```
**Solution:**
1. Ensure API server is running
2. Verify API_URL in `mobile_app.py` is correct
3. Check network connectivity
4. Test API: http://localhost:8000/docs

### Module Not Found
```
ModuleNotFoundError: No module named 'flet'
```
**Solution:**
```bash
pip install -r requirements.txt
```

## 📋 Checklist

### Initial Setup
- [ ] Python 3.8+ installed
- [ ] MariaDB running
- [ ] Virtual environment created
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Database setup: `python setup_database.py`

### Running the Project
- [ ] Start API: `uvicorn to_do_list:app --reload`
- [ ] API accessible: http://localhost:8000/docs
- [ ] Start Mobile App: `python mobile_app.py`
- [ ] Mobile app loads in browser

### Testing
- [ ] Run API tests: `python test_api.py`
- [ ] Access Swagger UI
- [ ] Test Users endpoint
- [ ] Test Tasks endpoint
- [ ] Test Mobile app buttons

## 🚀 Deployment

### Development
```bash
uvicorn to_do_list:app --reload
```

### Production
```bash
uvicorn to_do_list:app --host 0.0.0.0 --port 8000 --workers 4
```

### Mobile Deployment
```bash
# Create iOS app
flet publish ios

# Create Android app
flet publish android

# Create Web app
flet build web
```

## 📚 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Flet Docs](https://flet.dev)
- [Pydantic Docs](https://docs.pydantic.dev)
- [MariaDB Docs](https://mariadb.com/docs)

## 🔐 Security Notes

⚠️ **Important for Production:**

1. **Password Hashing**: Implement bcrypt for passwords
2. **Authentication**: Add JWT tokens
3. **CORS**: Configure for your frontend domain
4. **HTTPS**: Use in production
5. **Environment Variables**: Store secrets in `.env`
6. **Database**: Use strong passwords, limit access

## 📝 License

Open source project

## 👨‍💻 Author Notes

This project demonstrates:
- ✅ RESTful API design with FastAPI
- ✅ Database integration with ORM
- ✅ Mobile UI with Flet framework
- ✅ Async/await patterns
- ✅ Error handling and validation
- ✅ Project structure and organization

## 🎓 Next Steps

1. ✅ Customize the UI colors and styles
2. ✅ Add authentication (JWT)
3. ✅ Add data validation
4. ✅ Deploy to cloud (Heroku, AWS, GCP)
5. ✅ Add WebSocket for real-time updates
6. ✅ Create mobile app in App Store/Play Store

---

**Happy coding! 🎉**

For questions or issues, refer to the detailed documentation files included in the project.
