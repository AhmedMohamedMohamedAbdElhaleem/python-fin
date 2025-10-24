

from user_manager import UserManager
from transaction_manager import TransactionManager

def main_menu():
    um = UserManager()
    tm = TransactionManager(um)

    while True:
        print("\n===  PERSONAL FINANCE MANAGER ===")
        print("1. Register new user")
        print("2. Login")
        print("3. Show current user")
        print("4. Transactions menu")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            um.register_user()
        elif choice == "2":
            um.login()
        elif choice == "3":
            um.show_current_user()
        elif choice == "4":
            transaction_menu(tm)
        elif choice == "0":
            print("thanks - Goodbye!")
            break
        else:
            print(" Invalid choice.")

def transaction_menu(tm):
    while True:
        print("\n---  TRANSACTIONS MENU ---")
        print("1. Add income/expense")
        print("2. View all transactions")
        print("3. Edit transaction")
        print("4. Delete transaction")
        print("0. Back to main menu")

        choice = input("Choose: ").strip()

        if choice == "1":
            tm.add_transaction()
        elif choice == "2":
            tm.view_transactions()
        elif choice == "3":
            tm.edit_transaction()
        elif choice == "4":
            tm.delete_transaction()
        elif choice == "0":
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    main_menu()
