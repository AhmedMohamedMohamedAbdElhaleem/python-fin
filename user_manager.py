


from getpass import getpass
from data_manager import DataManager

class UserManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.users = self.data_manager.load_data()
        self.current_user = None

    def save(self):
        self.data_manager.save_data(self.users)

    def register_user(self):
        username = input("Enter new username: ").strip()
        pin = getpass("Set 4-digit PIN: ").strip()

        if any(u["username"] == username for u in self.users):
            print("Username already exists.")
            return

        if len(pin) != 4 or not pin.isdigit():
            print("PIN must be 4 digits.")
            return

        new_user = {
            "username": username,
            "pin": pin,
            "transactions": []
        }
        self.users.append(new_user)
        self.save()
        print(" User registered successfully!")

    def login(self):
        username = input("Enter username: ").strip()
        pin = getpass("Enter PIN: ").strip()

        for u in self.users:
            if u["username"] == username and u["pin"] == pin:
                self.current_user = u
                print(f"Welcome back, {username}!")
                return
        print(" Invalid credentials.")

    def show_current_user(self):
        if self.current_user:
            print(f"Current user: {self.current_user['username']}")
        else:
            print("No user logged in.")


            
