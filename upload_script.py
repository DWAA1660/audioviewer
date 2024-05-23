import os
import time
import requests

# Define the directory to monitor

UPLOAD_URL = "http://localhost:5000/upload"  # Change this to your server address
DIRECTORY = "/home/david/Desktop/songs"

def upload_file(fullname, filename):
    files = {'file': open(os.path.join(os.path.join(DIRECTORY), fullname), 'rb')}
    print(fullname)
    response = requests.post(UPLOAD_URL, files=files, data={"name": fullname})
    if response.status_code == 200:
        print(f"File '{filename}' uploaded successfully.")
    else:
        print(f"Failed to upload file '{filename}'.")


def check_and_upload_files():
    
    # Get the list of files in the directory
    prefix_length = len(DIRECTORY) + 1
    for root, _, files in os.walk(DIRECTORY):
        for file in files:   
            # Check if file is already uploaded
            full_name = os.path.join(root, file)[prefix_length:]
            response = requests.get(f"http://localhost:5000/checkfile/?name={full_name}")
            if response.status_code == 202:
                print(f"File '{file}' not uploaded. Uploading now...")
                upload_file(full_name, file)


if __name__ == "__main__":
    while True:
        check_and_upload_files()
        time.sleep(60)  # Check every minute
