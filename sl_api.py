# Connect with soccerlab API using basic authentication method
# Perf 
# LFV: https://lfv.soccerlab.com/APIRest/v0.2/

# %%
import requests
import pandas as pd
import matplotlib.pyplot as plt


# %%
# API endpoint
url = "https://lfv.soccerlab.com/APIRest/v0.2/masterdata/seasonal_teams/seasonal_team_flattened9"

# %%

# Your login credentials (replace these with your actual username and password)
authentication = ('SL_Consultant','S!6biYWe9q5KN*t^^ZE@')

# --- Query Parameters ---
params = {
    "start_date": "2024-07-01",
    "end_date": "2025-06-30"
}

# --- Headers ---
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.get(url, auth=authentication, headers = headers, params = params)
print(response)

# %%
# Handle response
if response.status_code == 200:
    print("Success!")
elif response.status_code == 401:
    print("Authentication failed")
else:
    print(f"Another error occurred: {response.status_code}")
    print(response.text)

# %%
print(response.text)
print(response.headers.get("Content-Type"))
data = response.json()
# print(data)

# %%
records = data.get("Response", [])
df_sl = pd.json_normalize(records)
# Show top rows
print(df_sl.head(10))



# %%
print(df_sl.head(10))

# %%
# Exploratory analysis
col_names = pd.DataFrame(df_sl.columns, columns=["Column Names"])

# col binning
df_sl['AgeCategory'].value_counts()

# col filtering
u17_teams = df_sl[df_sl['AgeCategory'] == 'U17']
print(u17_teams[['Name', 'ClubName', 'SeasonName']])

# export to csv, excel 
# df_sl.to_excel("soccerlab_teams.xlsx", index=False)
# df_sl.to_csv("soccerlab_teams.csv", index=False)

# quick visualisation 
df_sl['SeasonName'].value_counts().plot(kind='bar')
plt.title("Teams per Season")
plt.ylabel("Count")
plt.show()

# %%


