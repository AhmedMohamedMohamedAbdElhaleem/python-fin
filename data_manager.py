import json
import csv
import os
import shutil
from datetime import datetime

class DataManager:
    def __init__(self, file_path="data/users.json", backup_dir="data/backup"):
        self.file_path = file_path
        self.backup_dir = backup_dir
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    # Load data on startup
    def load_data(self):
        if not os.path.exists(self.file_path):
            print("No saved data found ")
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(" Data loaded successfully.")
                return data
        except json.JSONDecodeError:
            print(" Corrupted data file. Starting new session.")
            return []

    #  Save to JSON (main)
    def save_data(self, users):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4)
            print(" Data saved successfully.")
            self.create_backup()  # Auto backup after each save
        except Exception as e:
            print(f" Error saving data: {e}")

    #  Save to CSV (optional export)
    def export_to_csv(self, users, file_name="/home/ahmed/Desktop/py-project/backup/transactions_export.csv"):
        try:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, "w", newline='', encoding="utf-8") as csvfile:
                fieldnames = ["username", "type", "amount", "category", "date", "note"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for user in users:
                    username = user["username"]
                    for t in user.get("transactions", []):
                        row = {
                            "username": username,
                            "type": t["type"],
                            "amount": t["amount"],
                            "category": t["category"],
                            "date": t["date"],
                            "note": t["note"]
                        }
                        writer.writerow(row)

            print(f" Transactions exported to CSV: {file_name}")
        except Exception as e:
            print(f" Error exporting CSV: {e}")

    # Create backup copy
    def create_backup(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            shutil.copy(self.file_path, backup_file)
            print(f" Backup created: {backup_file}")
        except Exception as e:
            print(f" Backup failed: {e}")


            