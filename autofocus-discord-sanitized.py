import os
import time
import requests
from discord import File
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the folder to monitor and the Discord webhook URL
folder = 'NINA_AUTOFOCUS_DIR_PATH'
webhook_url = 'WEBHOOK_URL_FOR_YOUR_DISCORD_AF_CHANNEL'

# Function to upload file to Discord
def upload_to_discord(file_path):
    file_name = os.path.basename(file_path)
    files = {'file': open(file_path, 'rb')}
    data = {'content': f'New autofocus file uploaded: {file_name}'}
    response = requests.post(webhook_url, data=data, files=files)
    if response.status_code == 200:
        print("File uploaded successfully to Discord.")
    else:
        print(f"Failed to upload file to Discord: {response.text}")

# Event handler for file creation
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        upload_to_discord(event.src_path)

# Create the observer and register the event handler
observer = Observer()
observer.schedule(MyHandler(), path=folder, recursive=False)
observer.start()

try:
    print(f"Monitoring folder '{folder}' for JSON files...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
