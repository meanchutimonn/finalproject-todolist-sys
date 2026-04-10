"""
Database Setup Script
This script creates the required tables in the MariaDB database
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "192.168.100.23",
    "user": "root",  # Change this to your database user
    "password": "P@ssw0rd",  # Change this to your database password
    "database": "to_do_list"
}

def create_database():
    """Create the to_do_list database if it doesn't exist"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✓ Database '{DB_CONFIG['database']}' created or already exists")
        cursor.close()
        connection.close()
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False
    return True

def create_tables():
    """Create the user and task tables"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Create user table
        create_user_table = """
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_user_table)
        print("✓ 'user' table created or already exists")

        # Create task table
        create_task_table = """
        CREATE TABLE IF NOT EXISTS task (
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
        )
        """
        cursor.execute(create_task_table)
        print("✓ 'task' table created or already exists")

        connection.commit()
        cursor.close()
        connection.close()
        print("\n✓ Database setup completed successfully!")
        return True

    except Error as e:
        print(f"✗ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Starting database setup...\n")
    if create_database():
        create_tables()
    else:
        print("Failed to create database")
