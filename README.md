# MomoData Analysis Project
## Project Overview
This project transforms a dense XML archive of 1,600 MTN MoMo SMS transactions ranging from airtime purchases and bill payments to money transfers into a full-stack web app that reveals patterns, activity types, and transactional flows across Rwanda’s mobile money ecosystem. Exercising full-stack proficiency; backend workflows, structured data storage, and user interface design.

## Objectives aimed at when creating the project
- Parse and clean raw SMS data from XML files.
- Categorize transactions into the given types.
- Store structured data in a relational database.
- Build a user-friendly dashboard website that help to visualize the transactions in different formats.

## Features
- **Backend**:
  - Parses and cleans MoMo SMS XML data.
  - Stores processed data into a MySQL database.
  - Provides APIs to retrieve data using FastAPI.

- **Frontend**:
  - Dynamically displays data using JavaScript.
  - Allows filtering of transactional data based on user preferences.
  - Generates interactive charts for data visualization.

## Technologies Used

### Backend:
- **Python** (with FastAPI for API development)
- **MySQL** (for data storage)
- **XML Parsing Libraries** (for handling SMS data)

### Frontend:
- **HTML**
- **CSS**
- **JavaScript**

### Charts:
- Charting library used to display interactive visualizations (e.g., Chart.js or D3.js, if applicable)

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
    ├── schema.sql
    ├── utils.py
    ├── main.py
    ├── momo_dashboard.db
    ├── requirements.txt
    ├── unprocessed_sms.log
├── frontend
    ├── index.html
    ├── main.js
    ├── styles.css
```


## Installation

### Prerequisites:
- Python 3.12+
- PostgreSQL
- MySQL Server
- FastApi
- Flask

### Steps to launching the project:
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

## Usage
1. Upload your XML data to the backend via the provided endpoint or interface.
2. The backend will parse, clean, and store the data in the MySQL database.
3. Use the frontend interface to:
   - View transactional data.
   - Apply filters to retrieve specific data.
   - Visualize data using charts.

## API Endpoints
| Method | Endpoint            | Description               |
|--------|-------------------  |---------------------------|
| `GET`  | `/sms?search=`      | search any word           |
| `GET`  | `/sms?type=`        | Retrieve filtered data    |
| `GET`  | `/sms?date=`        | Retrieve filtered data    |
| `GET`  | `/sms?amount=`      | Retrieve filtered data    |

## Filtering
The frontend allows users to filter data by various criteria such as:
- Date Range
- Filter by any word
- Transaction Type
- Amount

## Charts
Interactive charts provide insights into:
- Total transactions over time.
- Distribution of transaction types.
- Monthly transaction summaries.

## Collaborators of the Project
Amanda Leslie INEMA

Louis Marie Toussaint TONA

Ange UMUTONI

Olivier ITANGISHAKA

## Links to other parts of the project
- **Demonstration video link**:
https://drive.google.com/file/d/1pcrFpkqy2_aoKc4a2sjHtYNUKJzOmOK5/view?usp=sharing

- **Project report link**:
https://docs.google.com/document/d/1KMjd8-TMeAmjDXD6qfU5caxfX96HYlKoCs7RRkP3zCw/edit?usp=sharing
