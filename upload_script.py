import os
import time
import requests
from config import DIRECTORY, URL
# Define the directory to monitor
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY_UPLOAD")
print(KEY, 2)
def upload_file(fullname, filename):
    files = {'file': open(os.path.join(os.path.join(DIRECTORY), fullname), 'rb')}
    print(fullname)
    response = requests.post(f"{URL}/upload", files=files, data={"name": fullname}, headers={"key": KEY}, timeout=60)
    if response.status_code == 200:
        print(f"File '{filename}' uploaded successfully.")
    else:
        print(f"Failed to upload file '{filename}'. {response.status_code}")


def check_and_upload_files():
    
    # Get the list of files in the directory
    prefix_length = len(DIRECTORY) + 1
    for root, _, files in os.walk(DIRECTORY):
        for file in files:   
            # Check if file is already uploaded
            full_name = os.path.join(root, file)[prefix_length:]
            size = os.stat(f"{DIRECTORY}/{full_name}")
            response = requests.get(f"{URL}/checkfile/?name={full_name}&size={size.st_size}", timeout=60)
            if response.status_code == 202:
                print(f"File '{file}' not uploaded. Uploading now...")
                upload_file(full_name, file)


if __name__ == "__main__":
    while True:
        check_and_upload_files()
        time.sleep(60)  # Check every minute
