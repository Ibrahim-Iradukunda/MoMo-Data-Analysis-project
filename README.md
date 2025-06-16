📊 MoMo Data Analysis Project
Presentation Link: View Presentation

Welcome to the MoMo Data Analysis Project! This application allows you to analyze mobile money (MoMo) transaction data through interactive charts and a searchable table. It’s built with Flask (backend) and vanilla JavaScript/HTML/CSS (frontend), and supports XML uploads, pagination, and more.

🗂️ Project Structure
graphql
Copy
Edit
MoMo-Data-Analysis-project/
├── backend/               # Flask backend
│   ├── app.py             # Main Flask application
│   ├── create_db.py       # Initializes SQLite database
│   ├── insert_data.py     # Loads XML transaction data
│   ├── momo.db            # SQLite DB file
│   └── process_sms.py     # XML parsing logic
├── data/                  
│   └── momo_sms.xml       # Sample XML data
├── frontend/              # Frontend dashboard
│   ├── index.html         
│   ├── script.js          
│   └── style.css          
├── README.md              # This file
├── start_project.py       # Automation script
└── venv/                  # Virtual environment
🔄 How It Works
Backend (Flask)
API runs on http://127.0.0.1:5000/

Parses and loads XML data into SQLite DB

Provides endpoints for:

Fetching transactions

Searching by date/type

Uploading XML files

Frontend
Runs on http://0.0.0.0:8000/

Displays:

Transaction table

Pie chart: Transaction types

Bar chart: Monthly trends

Supports:

XML file uploads

Pagination (5 per page)

Search by date/type

Automation
start_project.py:

Starts backend and frontend servers

Opens the dashboard in your browser

🚀 Requirements
Python 3.13+

pip

git (optional)

Internet (for dependencies)

🔧 Installation (Option 1: Auto Start)
bash
Copy
Edit
git clone https://github.com/Ibrahim-Iradukunda/MoMo-Data-Analysis-project.git
cd MoMo-Data-Analysis-project

python3 -m venv myenv
source myenv/bin/activate

pip install flask flask-cors requests

python start_project.py
🔧 Installation (Option 2: Manual Backend Start)
bash
Copy
Edit
git clone https://github.com/Ibrahim-Iradukunda/MoMo-Data-Analysis-project.git
cd MoMo-Data-Analysis-project/backend

# Clean slate (optional)
rm momo.db

# Setup DB
python create_db.py

# Insert XML data
python insert_data.py
Make sure your XML file is available at:

python
Copy
Edit
XML_PATH = '../data/momo_sms.xml'
Then start the backend:

bash
Copy
Edit
python app.py
Open the frontend manually at http://localhost:8000/

🖥️ Running the App
bash
Copy
Edit
cd MoMo-Data-Analysis-project
source venv/bin/activate
python3 start_project.py
Flask backend: http://127.0.0.1:5000/

Dashboard frontend: http://0.0.0.0:8000/

📊 Dashboard Features
🔍 Search by date (YYYY-MM-DD) or transaction type (Airtime, Payment, etc.)

📂 Upload new XML data

📈 Visualize:

Pie Chart: Transaction types

Bar Chart: Monthly activity

📄 Paginated Table: 5 transactions per page

❌ Troubleshooting
Issue	Solution
python3: not found	Run which python3 or install Python: sudo apt install python3
Port already in use	Change ports in app.py or start_project.py
Data not loading	Ensure XML is placed correctly and XML_PATH is valid
Browser didn’t open	Manually visit: http://localhost:8000/

🙌 Contributing
Fork the repository

Create a new branch (git checkout -b feature-branch)

Make your changes

Commit and push (git commit -m "your message")

Submit a pull request

Bug reports and suggestions are welcome!

📄 License
Licensed under the MIT License. See LICENSE for more info.

🚀 Built With
Flask

Chart.js

HTML/CSS/JavaScript

Python 3.13+

