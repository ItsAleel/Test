import requests
import os
from pathlib import Path

# Constants
REPO_OWNER = 'ItsAleel'
REPO_NAME = 'Test'
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"

# Set the download path to be the same directory as the script
SCRIPT_DIRECTORY = Path(__file__).parent
DOWNLOAD_PATH = SCRIPT_DIRECTORY / "downloads"

# Ensure the download directory exists
DOWNLOAD_PATH.mkdir(exist_ok=True)

def get_latest_release():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch the latest release information: {response.status_code}")
        return None

def download_asset(asset_url, asset_name):
    response = requests.get(asset_url, stream=True)
    if response.status_code == 200:
        asset_path = DOWNLOAD_PATH / asset_name
        with open(asset_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {asset_name}")
    else:
        print(f"Failed to download asset {asset_name}: {response.status_code}")

def update_program():
    latest_release = get_latest_release()
    if latest_release and latest_release.get('assets'):
        for asset in latest_release['assets']:
            asset_name = asset['name']
            asset_url = asset['browser_download_url']
            local_asset_path = DOWNLOAD_PATH / asset_name
            
            # Only download if the file doesn't exist or you want to overwrite it
            if not local_asset_path.is_file():
                download_asset(asset_url, asset_name)
            else:
                print(f"{asset_name} already exists. Skipping download.")
    else:
        print("No new assets to download or release information is missing.")

if __name__ == "__main__":
    update_program()
