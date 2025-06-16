MomoData Analysis Dashboard

📊 Project Overview
This project transforms a dense XML archive of 1,600 MTN MoMo SMS transactions ranging from airtime purchases and bill payments to money transfers into a full-stack web app that reveals patterns, activity types, and transactional flows across Rwanda’s mobile money ecosystem. Exercising full-stack proficiency; backend workflows, structured data storage, and user interface design.

🎯 Objectives
Parse and clean raw SMS data from XML files.
Categorize transactions into meaningful types.
Store structured data in a relational database.
Build a user-friendly web dashboard to visualize transaction insights.

🧩 Features
Backend Data Processing:

XML parsing and data extraction
Data cleaning and normalization (amounts, dates, text)
Categorization into transaction types (e.g., withdrawals, transfers, payments)
Database Integration:

Frontend Interactive Dashboard:

Search and filter transactions by type, date, or amount.
Examine detailed transaction records in a structured table.

🏗️ Tech Stack
Frontend: HTML, CSS, JS
Backend: Python (flask)
Database: Supabase
API tester: Swagger API

🗃️ Project Structure
├──Image
    ├── logo.png
├── backend
    ├── app.py
    ├── config.py
    ├── data_cleaning.py
    ├── db_setup.py
    ├── load_data.py
    ├── models.py
    ├── modified_sms_v2.xml
    ├── parse_xml.py
    ├── requirements.txt
    ├── schema.sql
    ├── utils.py
├── frontend
    ├── index.html
    ├── main.js
    ├── style.css


🚀 Setup Instructions
Clone the Repository
git clone https://github.com/louistona/momo-data-analysis.git

Open the directory
cd momo-data-analysis

Run your terminal

Activate the Scripts
.\venv\Scripts\activate

Install dependencies
pip install -r backend/requirements.txt

⚠️ To avoid errors, it is advised to delete the 'transactions.db' file already in the database before proceeding with the instructions.


Create your database structure
python backend/db_setup.py

Parse and load the data into the database
python backend/load_data.py

Launch the browser application
python backend/app.py

You can open the index.html in a web browser in order to be able to see the database changes on the main dashboard.

📝 Authors

Amanda Leslie INEMA

Louis Marie Toussaint TONA

Ange UMUTONI

Olivier ITANGISHAKA

📌 Additional links:
Demonstration video link
Project report link
https://docs.google.com/document/d/1KMjd8-TMeAmjDXD6qfU5caxfX96HYlKoCs7RRkP3zCw/edit?usp=sharing
