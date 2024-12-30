# CommitCrew - Baseball Statistics Web App

This repository contains a web application for managing and analyzing historical baseball data from **Lahman's Baseball Dataset**. The application is built with **Flask** and provides comprehensive features to view, filter, and manage statistics related to **batting**, **pitching**, and **fielding**.

---

## About Lahman's Baseball Dataset

Lahman's Baseball Dataset is a comprehensive collection of historical baseball data, spanning from **1871 to the present day**. It includes detailed statistics on players, teams, leagues, and their performance. In this project, the following tables are used:

- **`leagues`**: Information about baseball leagues.
- **`teams`**: Details about teams, including their names and IDs.
- **`master`**: Player demographic information, including names and player IDs.
- **`batting`**: Statistics related to batting performance.
- **`pitching`**: Statistics related to pitching performance.
- **`fielding`**: Statistics related to fielding performance.

---

## Features

- **CRUD Operations**:
  - Create, Read, Update, and Delete records for teams, master, batting, pitching, and fielding tables.
- **Dynamic Filters and Sorting**:
  - Filter data by **year**, **team**, **league**, or **player name/ID**.
  - Sort by **year**, **team** or various statistics (e.g., **Wins**, **Runs**, **Hits**, **Games Played**).
- **Pagination**:
  - Navigate large datasets with dynamic pagination.

---

## Getting Started

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/baseball-statistics-web-app.git
   cd baseball-statistics-web-app

2. **Install dependencies**: Install all required Python packages using pip:
   ```bash
   pip install -r requirements.txt

3. **Set up environment variables:** Create a .env file in the project root and populate it with the following variables:
   ```bash
    DB_HOST=<your-database-host>
    DB_USER=<your-database-username>
    DB_PASSWORD=<your-database-password>
    DB_NAME=<your-database-name>
    SECRET_KEY=<your-secure-random-key>

4. **Initialize the database:** Set up the database schema and populate it with initial data:
   ```bash
   python database/db_init.py init-db

5. **Run the application:** Start the Flask development server:
   ```bash
   flask run
The application will be available at http://127.0.0.1:5000/

---

## How to Use

1. **Access the Web App:**
- Navigate to http://127.0.0.1:5000/ in your web browser.
- Explore the Teams, Master, Batting, Pitching, and Fielding pages.

2. **Filter and Sort Data:**
- Use filters to narrow down records by year, team, league, or player.
- Sort data by column headers (e.g., **Year**, **Team**, **Wins**, **Runs**, **Hits**, **Games Played**).

3. **Perform CRUD Operations:**
- Use the **Add New Record** button to add new player statistics.
- Click the **Update** button next to a record to edit it.
- Use the **Delete** button to remove a record.

4. Navigate Large Data:
- Use pagination controls to navigate through large datasets.

---

## Repository Structure
```bash
  CommitCrew/
  ├── app/
  │   ├── models/           # Database models and query logic
  │   ├── static/           # CSS, JS, and static files
  │   ├── templates/        # HTML templates for the Flask app
  │   ├── __init__.py       # App initialization
  │   ├── db_init.py        # Database initialization script
  |   └── views.py          # Flask routes and views
  ├── csv/                  # CSV files for database population
  ├── .env.example          # Example environment variable file
  ├── requirements.txt      # List of dependencies
  ├── README.md             # Project documentation
  └── run.py                # Entry point for running the app
