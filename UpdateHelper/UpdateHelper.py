import requests
import os
import zipfile

zip_file_path = "UpdateHelperPackage.zip" 
extracted_folder_path = "../UpdateHelperPackage"

repo_url = "https://github.com/Daxaroodles/TTDependencies"
zip_url = f"{repo_url}/archive/refs/heads/main.zip"

response = requests.get(zip_url)

if response.status_code == 200:
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    print("Repository downloaded successfully.")
else:
    print("Failed to download the repository. HTTP Status:", response.status_code)
    exit(1)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path) 

os.remove(zip_file_path)

print(f"Extracted and deleted {zip_file_path}")
