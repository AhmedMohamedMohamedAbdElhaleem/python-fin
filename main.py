from user_manager import UserManager

def main_menu():
    um = UserManager()

    while True:
        print("\n===  USER MANAGEMENT SYSTEM ===")
        print("1. Register new user")
        print("2. Login")
        print("3. Show current user")
        print("4. Switch user")
        print("5. View all users")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            um.register_user()
        elif choice == "2":
            um.login()
        elif choice == "3":
            um.show_current_user()
        elif choice == "4":
            um.switch_user()
        elif choice == "5":
            um.view_users()
        elif choice == "0":
            print("Exiting the system. Goodbye!")
            break
        else:
            print(" Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()


