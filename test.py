import os

def list_files(directory):
    prefix_length = len(directory) + 1  # Length of directory path plus the separator
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)[prefix_length:]

directory = '/home/david/Desktop/songs'
for file in list_files(directory):
    print(file)
