import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Import PhotoImage
import threading
from backup_tool import backup, run_scheduler, start_watchdog
from pathlib import Path

custom_icon_path = Path("backup_icon.png")
class BackupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Auto Backup Tool")
        self.geometry("300x250")

        # Set the window icon
        self.set_icon()

        self.label = tk.Label(self, text="Auto Backup Tool", font=("Arial", 14))
        self.label.pack(pady=10)

        self.backup_button = tk.Button(self, text="Start Backup Now", command=self.start_backup)
        self.backup_button.pack(pady=5)

        self.schedule_button = tk.Button(self, text="Start Scheduler", command=self.start_scheduler)
        self.schedule_button.pack(pady=5)

        self.watchdog_button = tk.Button(self, text="Start Watchdog", command=self.start_watchdog)
        self.watchdog_button.pack(pady=5)

    def set_icon(self):
        """Set the window icon, using custom icon if available"""
        if custom_icon_path.exists():
            self.iconphoto(True, PhotoImage(file=custom_icon_path))
        else:
            # Optionally, you can use a default icon or do nothing
            print("Custom icon not found, using default icon if available")

    def start_backup(self):
        self.backup_button.config(state=tk.DISABLED)
        try:
            backup()
            messagebox.showinfo("Backup Complete", "Backup completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")
        finally:
            self.backup_button.config(state=tk.NORMAL)

    def start_scheduler(self):
        threading.Thread(target=run_scheduler, daemon=True).start()
        messagebox.showinfo("Scheduler", "Scheduler started, backups will run as scheduled.")

    def start_watchdog(self):
        threading.Thread(target=start_watchdog, daemon=True).start()
        messagebox.showinfo("Watchdog", "Watchdog started, it will monitor changes and trigger backups.")

if __name__ == "__main__":
    app = BackupApp()
    app.mainloop()
