## 🚀 Project: Automated Analytics ETL Pipeline (DE102)

### **Project Overview**

Designed and implemented a full-stack data engineering pipeline that automates the extraction, transformation, and loading (ETL) of social media performance metrics. The project transforms raw API data into an interactive Power BI dashboard for weekly business intelligence tracking.

### **Technical Stack**

* **Language:** Python (Pandas, Flask, Requests)
* **Database:** MySQL (Version 9.5)
* **Visualization:** Power BI (DAX, Power Query)
* **DevOps/Tooling:** Virtual Environments (`.venv`), Environment Variables (`python-dotenv`), REST API Simulation.

### **Key Features & Achievements**

* **Custom API Development:** Built a Mock REST API using **Flask** to simulate a live production environment, generating historical daily data (Revenue and Subscribers) from April 2025.
* **Automated "Self-Healing" ETL:** Developed a Python script that automatically detects, creates, and updates the MySQL database schema and tables if they are missing, ensuring 100% pipeline uptime.
* **Advanced Troubleshooting:** Successfully resolved a complex infrastructure conflict involving dual MySQL instances (v8.0 and v9.5) by diagnosing port assignments and service connectivity issues.
* **Data Integrity:** Implemented `UPSERT` logic (ON DUPLICATE KEY UPDATE) in the MySQL load phase to prevent data duplication while allowing for historical data corrections.
* **Business Intelligence:** Created a weekly performance dashboard in **Power BI**, utilizing **DAX** to transform daily granular data into actionable weekly growth trends.

---

### **Reflections / Problem Solving**

> "During development, I encountered a '1049 Unknown Database' error despite the database appearing in MySQL Workbench. I diagnosed this as an instance conflict between two local MySQL installations. By identifying the specific port for the 9.5 instance and updating the connection string, I successfully re-established the pipeline flow. This taught me the importance of service management and precise configuration in multi-instance environments."

---
