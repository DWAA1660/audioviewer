import os
import time
import requests
from security import safe_requests

# Define the directory to monitor
DIRECTORY_TO_MONITOR = "static/sources"
UPLOAD_URL = "http://localhost:5000/upload"  # Change this to your server address


def upload_file(filename):
    files = {'file': open(os.path.join(DIRECTORY_TO_MONITOR, filename), 'rb')}
    response = requests.post(UPLOAD_URL, files=files)
    if response.status_code == 200:
        print(f"File '{filename}' uploaded successfully.")
    else:
        print(f"Failed to upload file '{filename}'.")


def check_and_upload_files():
    # Get the list of files in the directory
    files = os.listdir(DIRECTORY_TO_MONITOR)
    
    for filename in files:
        # Check if file is already uploaded
        response = safe_requests.get(f"http://localhost:5000/checkfile/{filename}")
        if response.status_code == 201:
            print(f"File '{filename}' not uploaded. Uploading now...")
            upload_file(filename)


if __name__ == "__main__":
    while True:
        check_and_upload_files()
        time.sleep(60)  # Check every minute
