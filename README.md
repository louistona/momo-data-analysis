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
    ├── _init_.py
    ├── Makefile
    ├── main.py
    ├── pyproject.toml
    ├── momo_dashboard.db
    ├── poetry.lock
    ├── modified_sms_v2.xml
    ├── sms_processing.py
    ├── requirements.txt
    ├── unprocessed_sms.log
├── frontend
    ├── index.html
    ├── index.js
    ├── index.css
```


## Installation

### Prerequisites:
- Python 3.12+
- PostgreSQL
- MySQL Server
- FastApi

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/MoMOO.git
   cd MoMOO
   ```
2. Set up the backend:
   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     cd pro
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up your MySQL database and configure the connection in the backend settings.
   - Start the FastAPI server:
     ```bash
     uvicorn main:app --reload
     ```

3. Set up the frontend:
   - Open the `index.html` file in your preferred browser.
   - Ensure the frontend is properly connected to the backend APIs.

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
   https://drive.google.com/file/d/1zdsFQ5lSGJ7qmndKB7QGe7XoHjOx_ve4/view?usp=sharing

- **Project report link**:
https://docs.google.com/document/d/1KMjd8-TMeAmjDXD6qfU5caxfX96HYlKoCs7RRkP3zCw/edit?usp=sharing
