
## 🛠️ Step 1: Find your "Instance 95" Port

Most MySQL instances run on port **3306**, but since you have two, the second one (95) is likely on **3307** or **3308**.

1. Open **MySQL Workbench** and connect to **Instance 95**.
2. Look at the top of the tab or the "Session" information.
3. It should say something like `root@localhost:3307`.
4. **Note that number.** (If it just says `localhost`, try `3306` first). It is actually 3306,

---

## 🛠️ Step 2: Connect Power BI to MySQL

1. Open **Power BI Desktop**.
2. Click **Get Data** > **MySQL database**.
3. **Server:** Enter `127.0.0.1:3307` (Replace `3307` with the port you found in Step 1).
4. **Database:** `de102_analytics`
5. **Authentication:**
* Click the **Database** tab on the left.
* **User:** `root`
* **Password:** `******` (or your actual password).


6. Click **Connect**.

> **⚠️ If you get a "Connector/NET" Error:**
> Power BI doesn't always come with the MySQL driver. If it says "This connector requires one or more additional components," [download this driver](https://dev.mysql.com/downloads/connector/net/), install it, and **restart Power BI**.

---

## 🛠️ Step 3: Prepare the "Weekly" View

Your project requires **Weekly Performance Tracking**, but our database has **Daily** rows. We'll use a "Calculated Column" in Power BI to group them.

1. In Power BI, click the **Table View** icon on the far left.
2. Select your `fact_performance` table.
3. Click **New Column** at the top.
4. Paste this DAX formula:
```dax
Start of Week = 'de102_analytics fact_performance'[report_date] - WEEKDAY('de102_analytics fact_performance'[report_date], 2) +1

```


*This creates a new date column that represents the Monday of every week.*

---

## 🛠️ Step 4: Build the Dashboard

Now, let's create the visuals you'll present.

### Visual 1: Weekly Revenue Trend (Line Chart)

* **X-Axis:** `Start of Week`
* **Y-Axis:** `revenue` (Sum)
* **Legend:** `account_id`
* *Why:* This shows if accounts are growing or shrinking week-over-week.

### Visual 2: Subscriber Growth (Clustered Column Chart)

* **X-Axis:** `account_id`
* **Y-Axis:** `subscribers` (Average or Max)
* *Why:* This lets you compare the size of different accounts at a glance.

### Visual 3: Total Revenue KPI (Card)

* **Field:** `revenue` (Sum)
* *Why:* Every stakeholder wants to see the "Big Number" immediately.

---

## 🚀 Final Check: The "Live" Test

This is the ultimate test of a Data Engineer.

1. Keep Power BI open.
2. Go back to VS Code and run `python scripts/etl_pipeline.py`.
3. Go to Power BI and click the **Refresh** button in the top ribbon.

**If the numbers in your charts change automatically, you have successfully built a "Live Data Pipeline"!**

---
