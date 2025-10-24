from datetime import datetime

class SearchFilterManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    # Helper to get all transactions
    def _get_transactions(self):
        if not self.user_manager.current_user:
            print("Please login first.")
            return []
        return self.user_manager.current_user.get("transactions", [])

    # 1️1 Search by date range
    def search_by_date_range(self):
        transactions = self._get_transactions()
        if not transactions:
            print("No transactions found.")
            return

        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print(" Invalid date format.")
            return

        results = [
            t for t in transactions
            if start <= datetime.strptime(t["date"], "%Y-%m-%d") <= end
        ]

        self._display_results(results)

    # 2️2 Filter by category
    def filter_by_category(self):
        transactions = self._get_transactions()
        if not transactions:
            print("No transactions found.")
            return

        category = input("Enter category to filter by: ").strip().lower()
        results = [t for t in transactions if t["category"].lower() == category]

        self._display_results(results)

    # 3️3 Filter by amount range
    def filter_by_amount(self):
        transactions = self._get_transactions()
        if not transactions:
            print("No transactions found.")
            return

        try:
            min_amount = float(input("Enter minimum amount: ").strip())
            max_amount = float(input("Enter maximum amount: ").strip())
        except ValueError:
            print("Invalid amount input.")
            return

        results = [
            t for t in transactions
            if min_amount <= t["amount"] <= max_amount
        ]

        self._display_results(results)

    # 4️4 Sort results
    def sort_transactions(self):
        transactions = self._get_transactions()
        if not transactions:
            print("No transactions found.")
            return

        print("\nSort by:")
        print("1. Date (newest first)")
        print("2. Date (oldest first)")
        print("3. Amount (highest first)")
        print("4. Amount (lowest first)")
        choice = input("Choose sorting option: ").strip()

        if choice == "1":
            results = sorted(transactions, key=lambda x: x["date"], reverse=True)
        elif choice == "2":
            results = sorted(transactions, key=lambda x: x["date"])
        elif choice == "3":
            results = sorted(transactions, key=lambda x: x["amount"], reverse=True)
        elif choice == "4":
            results = sorted(transactions, key=lambda x: x["amount"])
        else:
            print(" Invalid choice.")
            return

        self._display_results(results)

    # Helper: display formatted results
    def _display_results(self, results):
        if not results:
            print("No matching transactions found.")
            return

        print("\n===  SEARCH RESULTS ===")
        for i, t in enumerate(results, start=1):
            print(f"{i}. [{t['type'].upper()}] {t['amount']} | {t['category']} | {t['date']} | {t['note']}")
        print("=========================")
        print(f"Total found: {len(results)} transaction(s).")


        