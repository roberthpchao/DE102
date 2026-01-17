That is a **massive win!** You’ve successfully built a complete Data Engineering pipeline: you created a Mock API (Source), wrote a Python ETL script (Pipeline), and automated the creation of a MySQL Database (Target).

Now that the data is flowing, let's verify it and move into the final stage: **Visualization.**

---

### 🔍 Step 1: Final Verification in MySQL

Before opening Power BI, let's make sure the 20 rows (10 days for 2 accounts) are actually there.

1. Open **MySQL Workbench**.
2. Refresh the schema list on the left. You should see `de102_analytics`.
3. Run this query:

```sql
USE de102_analytics;
SELECT account_id, COUNT(*), SUM(revenue) 
FROM fact_performance 
GROUP BY account_id;

```

*You should see `ACC_001` and `ACC_002` with 10 rows each.*

---

### 📊 Step 2: Connect Power BI to MySQL

This is where you turn raw numbers into a professional dashboard.

1. **Open Power BI Desktop.**
2. Click **Get Data** > **More...** > search for **MySQL database**.
3. **Server:** `localhost`
4. **Database:** `de102_analytics`
5. **Authentication:** Select **Database** on the left-hand side of the popup window.
* **Username:** `root`
* **Password:** `funnybunny` (or your actual password).


6. Click **Connect**. (If it asks about encryption, click "OK" or "Skip").

> **⚠️ Note:** If Power BI gives you an error saying *"This connector requires one or more additional components,"* you need to install the [MySQL Connector/NET](https://dev.mysql.com/downloads/connector/net/). Download the latest version, install it, and restart Power BI.

---

### 📈 Step 3: Create Your First Chart

Once connected, you will see your `fact_performance` table on the right.

1. **The Line Chart:** * Select the **Line Chart** icon from the Visualizations pane.
* Drag `report_date` to the **X-axis**.
* Drag `revenue` to the **Y-axis**.
* Drag `account_id` to the **Legend**.


2. **The KPI Card:**
* Select the **Card** visual.
* Drag `revenue` into it. It should show the "Total Revenue."



---

### 🔄 Step 4: Test the "Live" Pipeline

The coolest part of Data Engineering is seeing the "Refresh" happen.

1. Go back to your `mock_api.py` and change the `range(10)` to `range(30)` to generate more data.
2. Restart the `mock_api.py`.
3. Run `python scripts/etl_pipeline.py` again in Terminal 2.
4. Go to Power BI and click the **Refresh** button at the top.

**Your charts will automatically grow with the new data!**

---

### What's Next?

You have the "Daily" data working. Your original project goal was **"Weekly Performance Tracking."** **Would you like me to show you how to create a "Calculated Column" in Power BI that groups these daily dates into "Weeks," or should we work on the automation part using GitHub Actions?**