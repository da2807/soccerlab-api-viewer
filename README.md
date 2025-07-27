# ⚽ SoccerLab Streamlit API Viewer

This is a lightweight, user-friendly Streamlit app that allows users to query the SoccerLab API using customizable filters and download results as CSV or Parquet. It’s designed for performance staff, analysts, and coaches to explore seasonal team data quickly — without needing to write backend code.

---

## 🧰 Features

- Enter custom SoccerLab API URL
- Select date range (start and end)
- Load paginated API data into DuckDB
- View and filter using dropdown menus (up to 5 fields)
- Run custom SQL queries directly in the app
- Download filtered data as **CSV** or **Parquet**
- Responsive, wide layout with centered headings

---

## 🚀 How to Run the App

Make sure you have **Python 3.8+** and **Streamlit** installed.

### 1️⃣ Install dependencies

If using `requirements.txt`:

```bash
pip install -r requirements.txt

pip install streamlit duckdb pandas requests

streamlit run app.py

---

## 🔐 API Authentication

To access the SoccerLab API, you’ll need to add your credentials in a secure way.

Create a file called `secrets.toml` inside the `.streamlit` folder:

```toml
# .streamlit/secrets.toml

username = "your_soccerlab_username"
password = "your_soccerlab_password"

---

## 📁 Folder Structure
streamlit_app/
├── app.py # Main Streamlit app
├── requirements.txt # Dependencies
├── .gitignore # Ignore rules for Git
├── README.md # Documentation
├── .streamlit/
│ └── secrets.toml # API credentials (excluded from Git)
├── duckdb_loader.py # (If applicable) DuckDB data loading functions
├── api_utils.py # (If applicable) API helper functions
└── data/ # (Optional) Local data files

---

## 🛠️ To Do

- Add multi-select filter support
- Add user login or session-based access
- Improve error handling for API responses
- Support additional SoccerLab endpoints
- Option to schedule daily data pulls

---

## 📄 License

This project is private and intended for internal use at EDGE10.  
Contact the author for questions or collaboration.
