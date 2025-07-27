import requests
import pandas as pd
import math
import io
import streamlit as st
from datetime import datetime
import time
import duckdb
import os

# --- Streamlit App Config ---
st.set_page_config(page_title="SoccerLab API Viewer", layout="wide")

# --- Custom Header (Clean + Modern) ---
st.markdown("""
    <h1 style='text-align: center; font-size: 2.2rem;'>SoccerLab API Viewer</h1>
    <p style='text-align: center; color: grey;'>Query, filter, and download performance data with ease</p>
    <hr style='border:1px solid #e0e0e0; margin-top: 10px;'>
""", unsafe_allow_html=True)

# --- API Form ---
st.markdown("### API Settings")
with st.form("api_form"):
    api_url = st.text_input("Enter Full API URL", value="")
    username = st.text_input("API Username")
    password = st.text_input("API Password", type="password")
    start_date = st.date_input("Start Date", value=datetime(2024, 7, 1))
    end_date = st.date_input("End Date", value=datetime(2025, 6, 30))
    limit = st.number_input("Limit per page", value=50, step=10, min_value=10)
    submitted = st.form_submit_button("🔄 Fetch and Load Data")

st.markdown("---")

# --- Fetch Data and Store in Session State ---
if submitted and api_url:
    if not username or not password:
        st.warning("⚠️ Please enter both username and password.")
        st.stop()

    auth = (username, password)
    headers = {"Accept": "application/json"}

    if "group_training" in api_url or "CreatedWhen" in api_url:
        date_param_from = "CreatedWhen_from"
        date_param_to = "CreatedWhen_to"
    else:
        date_param_from = "start_date"
        date_param_to = "end_date"

    base_params = {
        date_param_from: start_date.strftime("%Y-%m-%d"),
        date_param_to: end_date.strftime("%Y-%m-%d"),
        "start": 0,
        "limit": limit,
        "format": "json"
    }

    try:
        response = requests.get(api_url, headers=headers, auth=auth, params=base_params)
        if response.status_code == 401:
            st.error("❌ Authentication failed. Please check your username/password.")
            st.stop()
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"API request failed: {e}")
        st.stop()

    total_count = data.get("TotalCount", len(data.get("Response", [])))
    pages = math.ceil(total_count / limit)
    all_records = pd.json_normalize(data.get("Response", []))

    # --- Progress Bar ---
    progress_bar = st.progress(0)
    status_text = st.empty()
    start_time = time.time()

    for page in range(1, pages):
        percent_complete = int((page / pages) * 100)
        progress_bar.progress(percent_complete)
        status_text.text(f"⏳ Fetching page {page + 1} of {pages}...")

        offset = page * limit
        paginated_params = base_params.copy()
        paginated_params["start"] = offset

        try:
            paginated_resp = requests.get(api_url, headers=headers, auth=auth, params=paginated_params)
            paginated_resp.raise_for_status()
            page_data = paginated_resp.json().get("Response", [])
            if not page_data:
                break
            page_df = pd.json_normalize(page_data)
            all_records = pd.concat([all_records, page_df], ignore_index=True)
        except Exception as e:
            st.warning(f"⚠️ Failed at page {page + 1}: {e}")
            break

    elapsed = time.time() - start_time
    progress_bar.progress(100)
    status_text.text(f"✅ Finished fetching {len(all_records)} records in {elapsed:.2f} seconds.")
    st.session_state["api_data"] = all_records

# --- Use Stored Data ---
if "api_data" in st.session_state and not st.session_state["api_data"].empty:
    all_records = st.session_state["api_data"]

    # --- Filter Section ---
    st.markdown("### Filter Data (Optional)")
    filter_cols = st.multiselect(
        "Select up to 5 columns to filter by", 
        options=all_records.columns.tolist(),
        max_selections=5
    )

    filters = {}
    for col in filter_cols:
        unique_vals = all_records[col].dropna().unique().tolist()
        selected_vals = st.multiselect(f"Filter values for `{col}`", unique_vals)
        if selected_vals:
            filters[col] = selected_vals

    for col, selected_vals in filters.items():
        all_records = all_records[all_records[col].isin(selected_vals)]

    st.markdown("---")

    # --- SQL Section ---
    st.markdown("### SQL Query Editor")
    use_sql = st.checkbox("Enable SQL Editor")

    if use_sql:
        con = duckdb.connect()
        con.register("api_data", st.session_state["api_data"])
        default_sql = "SELECT * FROM api_data LIMIT 10"
        user_sql = st.text_area("Write your SQL query", value=default_sql, height=150)

        try:
            all_records = con.execute(user_sql).fetchdf()
            st.success("✅ SQL query executed successfully.")
        except Exception as e:
            st.error(f"SQL error: {e}")
            all_records = pd.DataFrame()

    st.markdown("---")

    # --- Data Preview ---
    st.markdown("### Data Preview")
    st.dataframe(all_records, use_container_width=True)

    st.markdown("---")

    # --- Download Section ---
    st.markdown("### Export Options")
    st.download_button("⬇️ Download as CSV", data=all_records.to_csv(index=False), file_name="api_data.csv", mime="text/csv")

    parquet_buffer = io.BytesIO()
    all_records.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    st.download_button("⬇️ Download as Parquet", data=parquet_buffer, file_name="api_data.parquet", mime="application/octet-stream")

    st.markdown("---")

    # --- Save to OneDrive ---
    st.markdown("### Auto-Save to OneDrive (for Power BI Sync)")
    try:
        output_folder = r"C:\Users\Aishwar\OneDrive - EDGE10 (UK) Ltd\Clients & Support - Export_Test_Python"
        os.makedirs(output_folder, exist_ok=True)

        csv_path = os.path.join(output_folder, "soccerlab_data.csv")
        parquet_path = os.path.join(output_folder, "soccerlab_data.parquet")

        all_records.to_csv(csv_path, index=False)
        all_records.to_parquet(parquet_path, index=False)

        st.success(f"✅ Files saved to OneDrive folder: {output_folder}")
    except Exception as e:
        st.error(f"❌ Failed to write to OneDrive: {e}")

