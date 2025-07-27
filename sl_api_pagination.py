# Connect with soccerlab API using basic authentication method
# Perf 
# LFV: https://lfv.soccerlab.com/APIRest/v0.2/

# %%
import requests
import pandas as pd
from datetime import date
import time


# %%
# API endpoint
url = "https://lfv.soccerlab.com/APIRest/v0.2/masterdata/seasonal_teams/seasonal_team_flattened9"

# %%
# define params, headers

# Your login credentials (replace these with your actual username and password)
authentication = ('SL_Consultant','S!6biYWe9q5KN*t^^ZE@')

# --- Query Parameters ---
params_base = {
    "start_date": "2024-07-01",
    "end_date": "2025-06-30",
    "format": "json"
}

# --- Headers ---
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


# --- First call to get total count ---
initial_params = params_base.copy()
initial_params.update({"start": 0, "limit": 50})

# %% 
# run response
response = requests.post(url, auth= authentication, headers=headers, params=initial_params)
result = response.json()

# %%
# Prepare Pagination
total_count = result.get("TotalCount", len(result.get("Response", [])))
limit = 50
pages = (total_count // limit) + (1 if total_count % limit > 0 else 0)

# Accumulate records
all_records = result.get("Response", [])

total_start = time.time() 
for page in range(1, pages):
    offset = page * limit
    paginated_params = params_base.copy()
    paginated_params.update({"start": offset, "limit": limit})

    res = requests.post(url, auth=authentication, headers=headers, params=paginated_params)
    res_data = res.json().get("Response", [])
    
    if not res_data:
        break
    
    all_records.extend(res_data)
    print(f"Fetched page {page + 1} with {len(res_data)} records")

loop_time = time.time() - total_start
print(f"Total time to process pages: {loop_time:.2f} seconds")

# %%
# To Dataframe
df_sl = pd.json_normalize(all_records)
# View output
print(f"Total records fetched: {len(df_sl)}")
print(df_sl.head(10))

# %%
# save in csv
filename = f"soccerlab_data_{date.today()}.csv"
df_sl.to_csv(filename, index=False)

