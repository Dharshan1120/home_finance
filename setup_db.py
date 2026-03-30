import pymysql
from app import app
from models import db

def create_database():
    try:
        # Connect to MySQL server (XAMPP default without db)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # Create Database if it does not exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS home_finance")
            print("Database created or already exists: home_finance")
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        print("Please ensure your XAMPP MySQL server is running properly.")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print("Setting up database...")
    create_database()
    
    # Initialize SQLAlchemy tables
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully.")
