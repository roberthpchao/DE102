### Step 1: Create the Folder & Open VS Code

1. Close your current VS Code window.
2. In Windows File Explorer, create a brand new folder: `C:\Users\Admin\Documents\Projects\DE102`.
3. Right-click that folder and select **Open with Code**.

---

### Step 2: Initialize the Virtual Environment (.venv)

1. Open a new Terminal in VS Code (**Ctrl + `**).
2. Type this command to create the environment:
```powershell
python -m venv .venv

```


3. **Activate it:**
```powershell
.venv\Scripts\activate

```


*You should now see `(.venv)` at the start of your terminal line.*

---

### Step 3: Install All Libraries Once

In that same terminal, install everything we need for the whole project:

```powershell
pip install flask requests pandas mysql-connector-python python-dotenv

```

---

### Step 4: Create the Project Structure

Create these files and folders in the VS Code sidebar so it looks like this:

* `DE102/`
* `scripts/`
* `etl_pipeline.py`


* `mock_api.py`
* `.env`
* `.gitignore`



---

### Step 5: Configure the `.env` File

Open `.env` and paste this. **Check your password carefully.** 

```text
DB_HOST=localhost
DB_USER=root
DB_PASS=********
DB_NAME=de102_analytics
API_KEY=mock_secret_token

```

---

### Step 6: Create the Mock API (`mock_api.py`)

Paste this into `mock_api.py`. This is the "Data Source."

```python
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def generate_data(acc_id):
    data_list = []
    start_date = datetime(2025, 4, 1)
    for i in range(10): # Let's start with just 10 days to keep it simple
        date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        data_list.append({
            "date": date_str,
            "revenue": round(random.uniform(100, 500), 2),
            "subscribers_total": random.randint(1000, 1100)
        })
    return data_list

@app.route('/v1/metrics')
def get_metrics():
    acc_id = request.args.get('account_id', 'Unknown')
    return jsonify({
        "account_info": {"id": acc_id},
        "data": generate_data(acc_id)
    })

if __name__ == '__main__':
    app.run(port=5000)

```

---

### Step 7: Create the Robust ETL (`scripts/etl_pipeline.py`)

This version is "self-healing." It will create the database and table for you automatically.

```python
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

```

### Step 7.1: **Create `test_mysql.py` and paste this:**

```python
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

```

---

### 🛠️ How to run the test

1. Make sure your terminal shows `(.venv)`.
2. Type: `python test_mysql.py`

### What the results mean:

* **If it says ✅ SUCCESS:** Your username and password in `.env` are perfect. You can proceed to Step 8!
* **If it says ❌ Access Denied (1045):** Your password or username in `.env` is wrong.
* **If it says ❌ Can't connect to MySQL server (10061):** Your MySQL service is turned off. (You might need to start it via "Services" in Windows or MySQL Notifier).

---

### Step 8: The Moment of Truth

1. **Terminal 1:** Run `python mock_api.py`.
2. **Open Terminal 2:** (Click the `+` icon, ensure it says `(.venv)`).
3. **Terminal 2:** Run `python scripts/etl_pipeline.py`.

**Does it say "✅ Database 'de102_analytics' and table are ready" this time?**