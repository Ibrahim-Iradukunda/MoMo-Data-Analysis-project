# MoMo Data Analysis Project

Presentation's link :

Welcome to the **MoMo Data Analysis Project**! This application helps you analyze mobile money (MoMo) transaction data. It allows you to visualize transaction types, explore monthly trends, and filter transactions with pagination support.

---

## 🗂️ Project Structure

```
MoMo-Data-Analysis-project/
├── backend/               # Flask backend
│   ├── app.py             # Main Flask application
│   ├── create_db.py       # Initializes the SQLite database
│   ├── insert_data.py     # Loads XML transaction data into the DB
│   ├── momo.db            # SQLite database file
│   └── process_sms.py     # Parses and processes SMS XML
├── data/                  # XML files directory
│   └── momo_sms_test.xml  # Sample data (optional)
├── frontend/              # Dashboard files
│   ├── index.html         # Frontend UI
│   ├── script.js          # Logic and interactivity
│   └── style.css          # Styling
├── README.md              # This file
├── start_project.py       # Automation script
└── venv/                  # Python virtual environment
```

---

## 🔄 How the System Works

### Backend

* Powered by **Flask** at `http://127.0.0.1:5000/`
* Loads and processes SMS data from XML files
* Stores transactions in a **SQLite** database

### Frontend

* Runs at `http://0.0.0.0:8000/`
* Displays:

  * Table of transactions
  * Pie chart of transaction types
  * Bar chart of monthly activity
* Supports:

  * Date/type search
  * Pagination (5 per page)
  * Upload of new XML files

### Automation

The script `start_project.py`:

* Starts backend and frontend
* Opens your browser to the dashboard

---

## 🚀 Prerequisites

* Python 3.13+
* pip
* git (optional)
* Internet (for installing packages)

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ibrahim-Iradukunda/MoMo-Data-Analysis-project.git
cd MoMo-Data-Analysis-project
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
# For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask flask-cors requests
```

### 4. Initialize the Database

```bash
cd backend
python3 create_db.py
```

### 5. (Optional) Load Sample Data

* Put your XML file in `data/momo_sms_test.xml`
* Make sure `insert_data.py` references the correct path:

  ```python
  XML_PATH = '../data/momo_sms_test.xml'
  ```
* Then run:

  ```bash
  python3 insert_data.py
  ```

---

## 🚪 Running the Project

```bash
cd /path/to/MoMo-Data-Analysis-project
source venv/bin/activate
python3 start_project.py
```

* Backend: `http://127.0.0.1:5000/`
* Frontend: `http://0.0.0.0:8000/`

---

## 📊 Using the Dashboard

* **Search** by date (`2025-06-12`) or type (`Airtime`, `Payment`, etc.)
* **Pagination**: 5 transactions per page
* **Upload XML**: Click 📁 to update data
* **Charts**:

  * Pie: Transaction types
  * Bar: Monthly trends

---

## ❌ Troubleshooting

### "python3: not found"

* Check with: `which python3`
* Update `start_project.py` with full Python path if needed
* Or install Python:

  ```bash
  sudo apt update && sudo apt install python3
  ```

### Port Conflicts

* Modify ports in `app.py` and `start_project.py` (e.g., use 5001/8001)

### Data Not Loading?

* Ensure XML file is placed correctly
* Confirm `XML_PATH` is correct in `insert_data.py`

### Browser Not Opening?

* Open manually:

  * `http://localhost:8000/` or `http://127.0.0.1:8000/`

---

## 🙌 Contributing

* Fork the repo
* Create a new branch
* Commit your changes
* Submit a pull request
* Report bugs on GitHub

---

## 📄 License

MIT License — see `LICENSE` file for details

---

## 🚀 Built With

* [Flask](https://flask.palletsprojects.com/)
* [Chart.js](https://www.chartjs.org/)
* Python 3.13+

> Inspired by the growing need to analyze and understand mobile money transactions efficiently.

👥 Contributors

* Ibrahim IRADUKUNDA –-- i.ibrahim@alustudent.com
* Benjamin NIYOMUKIZA –-- b.niyomukiz@alustudent.com
* Allan HIRWA NDAMUKUNDA –-- h.allan@alustudent.com
* Benigne UWITONZE --- b.uwitonze@alustudent.com



