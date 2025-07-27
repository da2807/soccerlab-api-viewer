# %% import libraries
import requests
import pandas as pd
import duckdb
from datetime import datetime
import math
import time

# %% params, headers
# --- Connect to or create local DuckDB file ---
db_path = "C:/Users/Aishwar/Downloads/soccerlab_api/soccerlab.duckdb"
con = duckdb.connect(database=db_path, read_only=False)

# --- API Setup ---
url = "https://lfv.soccerlab.com/APIRest/v0.2/masterdata/seasonal_teams/seasonal_team_flattened9"
username = "SL_Consultant"
password = "S!6biYWe9q5KN*t^^ZE@"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

params_base = {
    "start_date": "2024-07-01",
    "end_date": "2025-06-30",
    "format": "json"
}

# %% initial set up
# --- First request to get TotalCount ---
initial_params = params_base.copy()
initial_params.update({"start": 0, "limit": 50})

response = requests.post(url, auth=(username, password), headers=headers, params=initial_params)
result = response.json()

# --- Pagination setup ---
total_count = result.get("TotalCount", len(result.get("Response", [])))
limit = 50
pages = math.ceil(total_count / limit)
print(f"Total pages: {pages}")

#%% running duckdb to collect records
# --- Create table on first page ---
first_page_df = pd.json_normalize(result.get("Response", []))
con.execute("CREATE TABLE IF NOT EXISTS seasonal_teams AS SELECT * FROM first_page_df LIMIT 0")
con.register("first_page_df", first_page_df)
con.execute("INSERT INTO seasonal_teams SELECT * FROM first_page_df")

#%% looping through the pages
# --- Loop through remaining pages ---
total_start = time.time() 

for page in range(1, pages):
    offset = page * limit
    paginated_params = params_base.copy()
    paginated_params.update({"start": offset, "limit": limit})

    res = requests.post(url, auth=(username, password), headers=headers, params=paginated_params)
    res_data = res.json().get("Response", [])

    if not res_data:
        print(f"No more data at page {page}")
        break

    df_page = pd.json_normalize(res_data)
    con.register("df_page", df_page)
    con.execute("INSERT INTO seasonal_teams SELECT * FROM df_page")
    print(f"Inserted page {page + 1} ({len(df_page)} rows)")

loop_time = time.time() - total_start
print(f"Total time to process pages: {loop_time:.2f} seconds")
print("All data successfully loaded into DuckDB!")

# %% example duckdb query
# --- Example: Query from DuckDB ---
example_query = con.execute("SELECT SeasonName, COUNT(*) AS team_count FROM seasonal_teams GROUP BY SeasonName").fetchdf()
print(example_query)

con.execute("SELECT * FROM seasonal_teams LIMIT 5").fetchdf()
con.close()

# %%
