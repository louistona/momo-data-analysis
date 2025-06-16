# MomoData Analysis Project
## Project Overview
This project transforms a dense XML archive of 1,600 MTN MoMo SMS transactions ranging from airtime purchases and bill payments to money transfers into a full-stack web app that reveals patterns, activity types, and transactional flows across Rwanda’s mobile money ecosystem. Exercising full-stack proficiency; backend workflows, structured data storage, and user interface design.

## Objectives aimed at when creating the project
- Parse and clean raw SMS data from XML files.
- Categorize transactions into the given types.
- Store structured data in a relational database.
- Build a user-friendly dashboard website that help to visualize the transactions in different formats.

## Functions and attributes of the project
**Backend Data Processing**:

- XML parsing and data extraction
- Data cleaning and normalization (amounts, dates, text)
- Categorization into transaction types (e.g., withdrawals, transfers, payments)
- Database Integration

**Frontend Interactive Dashboard**:

- Search and filter transactions by type, date, or amount.
- Examine detailed transaction records in a structured table.

## Tech used to create the project
- **Frontend**: HTML, CSS, JS
- **Backend**: Python (flask)
- **Database**: Supabase
- **API tester**: Swagger API

## Folder and File Structure
```bash
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
```

## Steps to launching the project
1. Clone the Repository
   ```bash
   git clone https://github.com/louistona/momo-data-analysis.git
   ```

2. Open the directory
   ```bash
   cd momo-data-analysis
   ```

3. Run your terminal

4. Activate the Scripts
   ```bash
   .\venv\Scripts\activate
   ```

5. Install dependencies
   ```bash
   pip install -r backend/requirements.txt
   ```
⚠️ To avoid errors, it is advised to delete the 'transactions.db' file already in the database before proceeding with the instructions.


6. Create your database structure
   ```bash
   python backend/db_setup.py
   ```

7. Parse and load the data into the database
   ```bash
   python backend/load_data.py
   ```

8. Launch the browser application
   ```bash
   python backend/app.py
   ```

9. You can open the index.html in a web browser in order to be able to see the database changes on the main dashboard.

## Collaborators of the Project
Amanda Leslie INEMA

Louis Marie Toussaint TONA

Ange UMUTONI

Olivier ITANGISHAKA

## Links to other parts of the project
- **Demonstration video link**:
   https://drive.google.com/file/d/1zdsFQ5lSGJ7qmndKB7QGe7XoHjOx_ve4/view?usp=sharing

- **Project report link**:
https://docs.google.com/document/d/1KMjd8-TMeAmjDXD6qfU5caxfX96HYlKoCs7RRkP3zCw/edit?usp=sharing
