import os
from getpass import getpass
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential

# Prompt for credentials
username = input("Enter your SharePoint email: ")
password = getpass("Enter your password (input hidden): ")

# SharePoint config
site_url = "https://edge10ltd.sharepoint.com/sites/CCS"
relative_folder_path = "Shared Documents/General/SoccerLab/Export_Test_Python"
local_file_path = "soccerlab_data_2025-07-25.csv"  # Or .csv

# Connect and upload
ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))

with open(local_file_path, "rb") as f:
    file_content = f.read()

upload_filename = os.path.basename(local_file_path)
target_folder = ctx.web.get_folder_by_server_relative_url(relative_folder_path)
target_folder.upload_file(upload_filename, file_content).execute_query()

print(f"✅ Uploaded '{upload_filename}' to SharePoint successfully.")
