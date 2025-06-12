MoMo Data Analysis Project
Welcome to the MoMo Data Analysis Project! This application allows you to analyze mobile money (MoMo) transaction data, visualize transaction types and monthly trends, and filter transactions by date and type with pagination. The project includes a backend API, a frontend dashboard, and automated startup scripts.
Project Structure
MoMo-Data-Analysis-project/
├── backend/              # Contains Flask backend files
│   ├── app.py           # Main Flask application
│   ├── create_db.py     # Initializes the SQLite database
│   ├── insert_data.py   # Loads transaction data from XML
│   ├── momo.db          # SQLite database file
│   └── process_sms.py   # Processes SMS transaction data
├── data/                # Directory for transaction XML files
│   └── momo_sms_test.xml # Sample transaction data (optional)
├── frontend/            # Contains frontend files
│   ├── index.html       # Main HTML file for the dashboard
│   ├── script.js        # JavaScript for interactivity and charts
│   └── style.css        # CSS for styling
├── README.md            # This file
├── start_project.py     # Script to start backend, frontend, and open browser
└── venv/                # Virtual environment for dependencies

How the System Works

Backend: A Flask server (running on http://127.0.0.1:5000/) provides APIs to fetch and upload transaction data stored in a SQLite database (momo.db). It processes XML files containing SMS transaction records.
Frontend: A web dashboard (running on http://0.0.0.0:8000/) displays transaction data in a table, with charts for transaction types and monthly trends. It supports searching by date or type and paginates results (5 transactions per page).
Data: Transactions are loaded from XML files (e.g., momo_sms_test.xml) with details like date, type (Airtime, Payment, Received, Deposit, Withdrawal, Other), amount, and balance.
Automation: The start_project.py script launches the backend, starts the frontend server, and automatically opens the browser to the dashboard.

Prerequisites

Python 3.13 or later (check with python3 --version)
pip (Python package manager)
git (optional, for version control)
Internet connection (for initial dependency installation)

Installation

Clone or Download the Project:

If using git, run:
git clone https://github.com/Ibrahim-Iradukunda/MoMo-Data-Analysis-project.git
cd MoMo-Data-Analysis-project




Set Up Virtual Environment:
cd /home/pc usename/MoMo-Data-Analysis-project
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install flask flask-cors requests


Initialize the Database:
cd backend
python3 create_db.py


Add Sample Data (Optional):

Place the momo_sms_test.xml file in the data/ directory (create it if it doesn’t exist).

Load the data:
python3 insert_data.py


Ensure XML_PATH in insert_data.py is set to ../data/momo_sms_test.xml.




Running the Project

Activate the Virtual Environment:
cd /home/pc_username/MoMo-Data-Analysis-project
source venv/bin/activate


Start the Project:
python3 start_project.py


This script:
Starts the Flask backend on http://127.0.0.1:5000/.
Starts the frontend server on http://0.0.0.0:8000/.
Automatically opens your default browser to http://0.0.0.0:8000/.


You should see the dashboard with transaction data (if pre-loaded) and charts.


Using the Dashboard:

Search: Enter a date (e.g., "2025-06-12") or transaction type (e.g., "Airtime") in the search bar to filter results.
Pagination: Use "Previous" and "Next" buttons to navigate through pages (5 transactions per page).
Upload Data: Click "📁 Upload XML" to select a new XML file (e.g., momo_sms_test.xml) to update the data. An alert will confirm the data is saved.
Charts: View the Pie chart for transaction types and Bar chart for monthly trends.


Stop the Project:

Press Ctrl+C in the terminal to stop the script and close the servers.



Troubleshooting

"python3: not found":

Check the Python 3 path with which python3 (e.g., /usr/bin/python3). Update start_project.py to use the full path if needed.
Install Python 3 if missing: sudo apt update && sudo apt install python3.


Port Conflicts:

If port 5000 or 8000 is in use, change them in app.py and start_project.py (e.g., to 5001 and 8001) and update webbrowser.open().


Data Not Loading:

Ensure momo_sms_test.xml is in the data/ directory and matches the expected format.
Check insert_data.py for the correct XML_PATH.


Browser Not Opening:

Manually open http://localhost:8000/ or http://127.0.0.1:8000/ if 0.0.0.0 fails.



Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Report issues on the GitHub page.
License
This project is licensed under the MIT License - see the LICENSE file for details (add a LICENSE file if desired).
Acknowledgments

Built with Flask, Chart.js, and Python 3.13.
Inspired by mobile money transaction analysis needs.


