"""
Configuration Module
Load database and API settings from environment variables or defaults
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.100.23"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "to_do_list")
}

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Print configuration on startup (for debugging)
if DEBUG:
    print(f"API Config - Host: {API_HOST}, Port: {API_PORT}")
    print(f"Database Config - Host: {DB_CONFIG['host']}, Database: {DB_CONFIG['database']}")
