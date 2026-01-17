import os
import requests
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def run_pipeline():
    # 1. Connect to MySQL Server (Not the DB yet!)
    print("Connecting to MySQL Server...")
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )
    cursor = conn.cursor()

    # 2. Create Database and Table
    db_name = os.getenv('DB_NAME')
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_performance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id VARCHAR(50),
            report_date DATE,
            revenue DECIMAL(10, 2),
            subscribers INT,
            UNIQUE KEY unique_rec (account_id, report_date)
        )
    """)
    print(f"✅ Database '{db_name}' and table are ready.")

    # 3. Extract & Load for 2 accounts
    for acc in ["ACC_001", "ACC_002"]:
        print(f"Syncing {acc}...")
        res = requests.get(f"http://127.0.0.1:5000/v1/metrics?account_id={acc}")
        if res.status_code == 200:
            data = res.json()
            for row in data['data']:
                sql = """INSERT INTO fact_performance (account_id, report_date, revenue, subscribers) 
                         VALUES (%s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE revenue=VALUES(revenue)"""
                cursor.execute(sql, (acc, row['date'], row['revenue'], row['subscribers_total']))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("🚀 All done! Check MySQL Workbench.")

if __name__ == "__main__":
    run_pipeline()