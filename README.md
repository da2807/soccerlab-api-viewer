# ⚽ SoccerLab Streamlit API Viewer

This is a lightweight, user-friendly Streamlit app that allows users to query the SoccerLab API using customizable filters and download results as CSV or Parquet. It’s designed for performance staff, analysts, and coaches to explore seasonal team data quickly without needing to write backend code.

## Motivation 

Power BI is great, but it struggles with APIs that use pagination especially when working with historical data over months or years. So I built a lightweight Streamlit app that lets us fetch the full dataset via API, apply filters or SQL if needed, and export it to Parquet/CSV. This makes Power BI run faster and gives us a quick way to explore data without re-fetching or writing slow Power Query loops


## Ideal Use Cases
✅ Building quick PoCs or dashboards from new APIs

✅ Exploring long-term trends (1–5 years of data)

✅ Prepping data before pushing into a proper ETL/dataflow

✅ Working around slow/noisy APIs without waiting minutes each refresh

---

## Features

- Enter custom SoccerLab API URL
- Select date range (start and end)
- Load paginated API data into DuckDB
- View and filter using dropdown menus (up to 5 fields)
- Run custom SQL queries directly in the app
- Download filtered data as **CSV** or **Parquet**
- Responsive, wide layout with centered headings


## To Do

- Support additional SoccerLab endpoints
- Option to schedule daily data pulls
- Build automation by scheduling the script and the let PBI fetch data

---

## License

This project is private and intended for internal use at EDGE10.  
Contact the author for questions or collaboration.

---

## How to Run the App

Make sure you have **Python 3.8+** and **Streamlit** installed.

### Install dependencies

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
