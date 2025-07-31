# Connect with Performance API using basic authentication method
# Perf 
# Oxford United: https://oxfordunited1893.edge10online.co.uk/api/entity/

# %%
import requests
import pandas as pd


# %%
# API endpoint
url = "https://mls1993.edge10online.com/api/entity"
# https://mls1993.edge10online.com/api/entity
# https://oxfordunited1893.edge10online.co.uk/api/entity/

# %%
# Your login credentials (replace these with your actual username and password)
authentication = ('edge10','loRWROgw0XtgMnnit0g6o2s2NKWIWJm6yYJIzpLCT0dyVvpvY7Sb5FPFA1QzuWN')

response = requests.get(url, auth=authentication)

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
data = response.json()
print(data)

# %%
df = pd.DataFrame(data)
print(df.head(10))


# %%
# With ContactType = 2
df_players = df[df['contactType']==2]
print(df_players)


# %%
df_players.to_csv("mls_users.csv", index=True)
# %%
