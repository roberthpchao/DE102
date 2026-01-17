import os
import mysql.connector
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def test_connection():
    print("--- MySQL Connection Test ---")
    try:
        # Attempt to connect to the SERVER (without database name first)
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
        
        if conn.is_connected():
            print("✅ SUCCESS: Python connected to the MySQL Server!")
            
            # Check if our database exists
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            print(f"Current Databases: {databases}")
            
            cursor.close()
            conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ ERROR: Could not connect to MySQL.")
        print(f"Details: {err}")

if __name__ == "__main__":
    test_connection()