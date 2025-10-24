

from user_manager import UserManager
from transaction_manager import TransactionManager
from report_manager import ReportManager
from search_filter_manager import SearchFilterManager



def main_menu():
    um = UserManager()
    tm = TransactionManager(um)
    rm = ReportManager(um)
    sf = SearchFilterManager(um)

    while True:
        print("\n=== PERSONAL FINANCE MANAGER ===")
        print("1. Register new user")
        print("2. Login")
        print("3. Show current user")
        print("4. View all users")           
        print("5. Switch user (re-login)")    
        print("6. Transactions menu")
        print("7. Reports menu")
        print("8. Search & Filter menu")
        print("9. Export to CSV")             
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            um.register_user()
        elif choice == "2":
            um.login()
        elif choice == "3":
            um.show_current_user()
        elif choice == "4":                   
            print("\n Registered Users:")
            for i, u in enumerate(um.users, 1):
                print(f"{i}. {u['username']}")
        elif choice == "5":                  
            um.login()
        elif choice == "6":
            transaction_menu(tm)
        elif choice == "7":
            report_menu(rm)
        elif choice == "8":
            search_filter_menu(sf)
        elif choice == "9":                   
            um.data_manager.export_to_csv(um.users)
        elif choice == "0":
            print(" Goodbye!")
            break
        else:
            print("Invalid choice.")




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

def report_menu(rm):
    while True:
        print("\n--- REPORTS MENU ---")
        print("1. Dashboard summary")
        print("2. Monthly report")
        print("3. Category breakdown")
        print("4. Spending trends")
        print("0. Back to main menu")

        choice = input("Choose: ").strip()

        if choice == "1":
            rm.dashboard_summary()
        elif choice == "2":
            rm.monthly_report()
        elif choice == "3":
            rm.category_breakdown()
        elif choice == "4":
            rm.spending_trends()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def search_filter_menu(sf):
    while True:
        print("\n---  SEARCH & FILTER MENU ---")
        print("1. Search by date range")
        print("2. Filter by category")
        print("3. Filter by amount range")
        print("4. Sort transactions")
        print("0. Back to main menu")

        choice = input("Choose: ").strip()

        if choice == "1":
            sf.search_by_date_range()
        elif choice == "2":
            sf.filter_by_category()
        elif choice == "3":
            sf.filter_by_amount()
        elif choice == "4":
            sf.sort_transactions()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()

    