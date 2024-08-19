import os
import logging
import json
from pathlib import Path
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import schedule
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Setup logging
logging.basicConfig(filename='backup.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Google Drive Authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Tracking file modification times
backup_history = {}

def scan_files_to_backup():
    """Scans the directories to find files to backup based on specified file types"""
    files_to_backup = []
    file_types = config.get('file_types', [])

    for folder in config['backup_folders']:
        p = Path(folder)
        if p.exists() and p.is_dir():
            if file_types:  # If specific file types are specified
                for file_type in file_types:
                    files_to_backup.extend(p.rglob(f'*{file_type}'))
            else:  # If no specific file types are specified, back up all files
                files_to_backup.extend(p.rglob('*.*'))
        else:
            logging.warning(f"Folder {folder} does not exist.")
    
    return files_to_backup

def trigger_backup(filepath):
    """Triggers backup if the file is new or has been modified"""
    last_modified_time = os.path.getmtime(filepath)
    if filepath not in backup_history or backup_history[filepath] < last_modified_time:
        backup_history[filepath] = last_modified_time
        upload_to_drive(filepath)

def upload_to_drive(file_path):
    """Uploads a file to Google Drive"""
    try:
        file_drive = drive.CreateFile({
            'title': file_path.name,
            'parents': [{'id': config['google_drive_folder_id']}]
        })
        file_drive.SetContentFile(file_path.as_posix())
        file_drive.Upload()
        logging.info(f"Uploaded {file_path} to Google Drive.")
    except Exception as e:
        logging.error(f"Failed to upload {file_path}: {e}")

def backup():
    """Backup process"""
    files = scan_files_to_backup()
    if not files:
        logging.info("No files to backup.")
        return

    for file in files:
        trigger_backup(file)
    logging.info("Backup completed successfully.")

# Scheduler setup
if config['backup_schedule'] == "daily":
    schedule.every().day.at("01:00").do(backup)
elif config['backup_schedule'] == "weekly":
    schedule.every().monday.at("01:00").do(backup)

def run_scheduler():
    """Run the scheduled tasks"""
    while True:
        schedule.run_pending()
        time.sleep(1)

class WatchdogHandler(FileSystemEventHandler):
    """Handler for monitoring file system events"""
    def on_modified(self, event):
        if not event.is_directory:
            file_types = config.get('file_types', [])
            if not file_types or any(event.src_path.endswith(ft) for ft in file_types):
                logging.info(f"Detected change in {event.src_path}, triggering backup.")
                trigger_backup(Path(event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            file_types = config.get('file_types', [])
            if not file_types or any(event.src_path.endswith(ft) for ft in file_types):
                logging.info(f"Detected new file {event.src_path}, triggering backup.")
                trigger_backup(Path(event.src_path))

def start_watchdog():
    """Start watchdog to monitor directories for changes"""
    event_handler = WatchdogHandler()
    observer = Observer()
    for folder in config['backup_folders']:
        observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
