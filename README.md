# Auto Backup Tool

## Description
A simple Python tool for automatically backing up files from your local PC to Google Drive. This tool allows you to specify which file types to back up, either all file types or specific ones, and supports both manual and scheduled backups via a simple GUI.

## Setup

### 1. Install Dependencies
Make sure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Google Drive Authentication

To allow the tool to access your Google Drive, you need to set up OAuth 2.0 authentication:

1. **Create a Project on Google Cloud Console**:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing one.
    - Navigate to "APIs & Services" > "Credentials".
    - Click "Create Credentials" and select "OAuth 2.0 Client ID".
    - Configure the OAuth consent screen if prompted.
    - Choose "Desktop App" as the application type and click "Create".
    - Download the `credentials.json` file and place it in the root directory of your project.
    - Ensure to rename it as `client_secrets.json`

2. **Authenticate the Application**:
    - When you run the tool for the first time, it will open a web browser for you to log in to your Google account and authorize the application.

### 3. Configure `config.json`

Configure the `config.json` file with your desired settings:

- **Google Drive Folder ID**: Specify the ID of the folder where backups will be stored. The folder ID is the part of the Google Drive URL that comes after `/folders/`. For example, in the URL `https://drive.google.com/drive/u/0/folders/23456-5WYPmhi0`, the folder ID is `23456-5WYPmhi0`.

```json
{
  "backup_folders": ["/Users/Documents/tests"],
  "folder_id": "23456-5WYPmhi0",
  "file_types": ["*.docx", "*.pdf", "*.xlsx"],
  "backup_interval": "daily"
}
```

- **Backup Folders**: Set the directories items for backup should be retrieved. You can add more than one folder (e.g. ["/Users/Documents/tests", "/Users/Documents/items"]).
- **File Types**: List the file types you want to back up. Leave this field empty to back up all file types.
- **Backup Interval**: Set the schedule for automatic backups (e.g., `daily`, `weekly`).

### 4. Run the GUI

- **Manual Backup**: Open the GUI and click the "Backup Now" button to start a backup immediately.
- **Scheduled Backup**: Open the GUI, configure the schedule, and start the scheduler to run backups automatically.

```bash
python gui.py
```

## Logs

Logs of backup activities are stored in `backup.log`. You can check this file for information on past backups and any errors that might have occurred.