from user_manager import UserManager
from transaction_manager import TransactionManager
from report_manager import ReportManager
from search_filter_manager import SearchFilterManager
from savings_goal_manager import SavingsGoalManager
from monthly_budget_manager import MonthlyBudgetManager
from notification_manager import NotificationManager


def main_menu():
    
    um = UserManager()
    tm = TransactionManager(um)
    rm = ReportManager(um)
    sf = SearchFilterManager(um)
    sg = SavingsGoalManager(um)
    bm = MonthlyBudgetManager(um)
    nm = NotificationManager(um)

    while True:
        print("\n=== PERSONAL FINANCE MANAGER ===")
        print("1) Register new user")
        print("2) Login")
        print("3) Show current user")
        print("4) View all users")
        print("5) Switch user")
        print("6) Transactions")
        print("7) Reports")
        print("8) Search & Filter")
        print("9) Export to CSV")
        print("10) Savings Goals")
        print("11) Monthly Budget")
        print("12) Notifications Center")
        print("0) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            um.register_user()
        elif choice == "2":
            um.login()
        elif choice == "3":
            um.show_current_user()
        elif choice == "4":
            print("\nRegistered Users:")
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
        elif choice == "10":
            savings_menu(sg)
        elif choice == "11":
            budget_menu(bm)
        elif choice == "12":
            nm.check_notifications()
        elif choice == "0":
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid choice, try again.")


def transaction_menu(tm):
    while True:
        print("\n--- Transactions ---")
        print("1) Add income/expense")
        print("2) View all transactions")
        print("3) Edit transaction")
        print("4) Delete transaction")
        print("0) Back")

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
            print("Invalid choice.")


def report_menu(rm):
    while True:
        print("\n--- Reports ---")
        print("1) Dashboard summary")
        print("2) Monthly report")
        print("3) Category breakdown")
        print("4) Spending trends")
        print("5) ASCII charts")
        print("0) Back")

        choice = input("Choose: ").strip()

        
        options = {
            "1": rm.dashboard_summary,     
            "2": rm.monthly_report,         
            "3": rm.category_breakdown,      
            "4": rm.spending_trends,         
            "5": rm.ascii_visualization     
        }

        if choice in options:
            print("\nGenerating report, please wait...\n")
            options[choice]()
            print("\nReport done ✔️")
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def search_filter_menu(sf):
    while True:
        print("\n--- Search & Filter ---")
        print("1) Search by date range")
        print("2) Filter by category")
        print("3) Filter by amount range")
        print("4) Sort transactions")
        print("0) Back")

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


def savings_menu(sg):
    while True:
        print("\n--- Savings Goals ---")
        print("1) Add goal")
        print("2) View goals")
        print("3) Allocate amount")
        print("4) Edit goal")
        print("5) Delete goal")
        print("0) Back")

        c = input("Choose: ").strip()
        if c == "1":
            sg.add_goal()
        elif c == "2":
            sg.view_goals()
        elif c == "3":
            sg.add_saved_amount()
        elif c == "4":
            sg.edit_goal()
        elif c == "5":
            sg.delete_goal()
        elif c == "0":
            break
        else:
            print("Invalid choice.")


def budget_menu(bm):
    while True:
        print("\n--- Monthly Budget ---")
        print("1) Set budget")
        print("2) View budget status")
        print("0) Back")

        c = input("Choose: ").strip()
        if c == "1":
            bm.set_budget()
        elif c == "2":
            bm.view_budget_status()
        elif c == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main_menu()
