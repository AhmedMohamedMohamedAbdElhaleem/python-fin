import json
import os

class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()
        self.current_user = None

    # Load users from file
    def load_users(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    # Save users to file
    def save_users(self):
        with open(self.filename, "w") as f:
            json.dump(self.users, f, indent=4)

    # Register new user
    def register_user(self):
        username = input("Enter new username: ").strip()
        pin = input("Enter 4-digit PIN: ").strip()

        if not pin.isdigit() or len(pin) != 4:
            print("PIN must be 4 digits only.")
            return

        for user in self.users:
            if user["username"] == username:
                print(" Username already exists.")
                return

        new_user = {
            "username": username,
            "pin": pin,
            "transactions": []
        }

        self.users.append(new_user)
        self.save_users()
        print(f"User '{username}' registered successfully!")

    # Login user
    def login(self):
        username = input("Enter username: ").strip()
        pin = input("Enter PIN: ").strip()

        for user in self.users:
            if user["username"] == username and user["pin"] == pin:
                self.current_user = user
                print(f"Login successful. Welcome {username}!")
                return True

        print(" Invalid username or PIN.")
        return False

    # View all users
    def view_users(self):
        if not self.users:
            print(" No users found.")
            return
        print("\n Registered Users:")
        for i, user in enumerate(self.users, start=1):
            print(f"{i}. {user['username']}")

    # Switch user
    def switch_user(self):
        self.view_users()
        choice = input("Enter user number to switch: ").strip()
        if not choice.isdigit():
            print(" Invalid input.")
            return
        index = int(choice) - 1
        if 0 <= index < len(self.users):
            self.current_user = self.users[index]
            print(f" Switched to user: {self.current_user['username']}")
        else:
            print(" Invalid user number.")

    # Show current user
    def show_current_user(self):
        if self.current_user:
            print(f" Current user: {self.current_user['username']}")
        else:
            print(" No user currently logged in.")




