import requests
import pandas as pd
import duckdb
from datetime import datetime
import math
import time
import streamlit as st
import io

# --- Streamlit App Title ---
st.set_page_config(page_title="SoccerLab Viewer", layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>⚽ SoccerLab Data Viewer</h1>
    <hr style='border:1px solid #ccc;'>
""", unsafe_allow_html=True)

# --- Connect to DuckDB ---
db_path = "C:/Users/Aishwar/Downloads/soccerlab_api/soccerlab.duckdb"
con = duckdb.connect(database=db_path, read_only=False)

# --- Query for dropdown options ---
seasons = con.execute("SELECT DISTINCT SeasonName FROM seasonal_teams ORDER BY SeasonName DESC").fetchdf()["SeasonName"].dropna().tolist()
ages = con.execute("SELECT DISTINCT AgeCategory FROM seasonal_teams ORDER BY AgeCategory").fetchdf()["AgeCategory"].dropna().tolist()

# --- Layout with filters ---
col1, col2 = st.columns(2)

# Season filter
season_options = ["All"] + seasons
with col1:
    selected_seasons = st.multiselect("Select Season(s)", options=season_options, default=["All"])

# AgeCategory filter
age_options = ["All"] + ages
with col2:
    selected_ages = st.multiselect("Select Age Category(s)", options=age_options, default=["All"])

# --- Build dynamic WHERE clause ---
where_clauses = []
if "All" not in selected_seasons:
    season_str = ",".join([f"'{s}'" for s in selected_seasons])
    where_clauses.append(f"SeasonName IN ({season_str})")
if "All" not in selected_ages:
    age_str = ",".join([f"'{a}'" for a in selected_ages])
    where_clauses.append(f"AgeCategory IN ({age_str})")

where_sql = "WHERE " + " AND " .join(where_clauses) if where_clauses else ""

query = f"""
    SELECT * FROM seasonal_teams
    {where_sql}
    ORDER BY ShortName
"""

# --- Custom SQL Query Input ---
st.markdown("### Advanced: Write Your Own SQL Query (optional)")
use_custom_sql = st.checkbox("Enable custom SQL editor")

if use_custom_sql:
    default_sql = f"SELECT * FROM seasonal_teams LIMIT 10"
    user_sql = st.text_area("Enter your SQL query:", value=default_sql, height=150)

    try:
        df_filtered = con.execute(user_sql).fetchdf()
        st.success("Query ran successfully!")
    except Exception as e:
        st.error(f"Error in SQL query: {e}")
        df_filtered = pd.DataFrame()
else:
    df_filtered = con.execute(query).fetchdf()

# --- Show Results ---
st.markdown("### Filtered Results")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

# --- Show metadata ---
st.markdown(f"<p style='text-align:right;'>Showing <b>{len(df_filtered)}</b> records</p>", unsafe_allow_html=True)

# --- Option to download CSV ---
st.download_button("Download CSV", data=df_filtered.to_csv(index=False), file_name="filtered_soccerlab_data.csv", mime="text/csv")

# --- Option to download Parquet ---
parquet_buffer = io.BytesIO()
df_filtered.to_parquet(parquet_buffer, index=False)
parquet_buffer.seek(0)
st.download_button("Download Parquet", data=parquet_buffer, file_name="filtered_soccerlab_data.parquet", mime="application/octet-stream")

# --- Optional: Disconnect ---
con.close()



