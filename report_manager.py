import datetime
from collections import defaultdict

class ReportManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    # Helper: get all transactions for current user
    def _get_transactions(self):
        if not self.user_manager.current_user:
            print(" Please login first.")
            return []
        return self.user_manager.current_user.get("transactions", [])

    #  Dashboard summary
    def dashboard_summary(self):
        transactions = self._get_transactions()
        if not transactions:
            print(" No transactions found.")
            return

        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        balance = total_income - total_expense

        print("\n===  DASHBOARD SUMMARY ===")
        print(f"Total Income:  {total_income:.2f}")
        print(f"Total Expense: {total_expense:.2f}")
        print(f"Net Balance:   {balance:.2f}")
        print("============================")

    #  Monthly reports
    def monthly_report(self):
        transactions = self._get_transactions()
        if not transactions:
            print("No transactions found.")
            return

        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.datetime.strptime(month, "%Y-%m")
        except ValueError:
            print(" Invalid month format.")
            return

        filtered = [t for t in transactions if t["date"].startswith(month)]
        if not filtered:
            print("No transactions for this month.")
            return

        income = sum(t["amount"] for t in filtered if t["type"] == "income")
        expense = sum(t["amount"] for t in filtered if t["type"] == "expense")
        balance = income - expense

        print(f"\n===  MONTHLY REPORT ({month}) ===")
        print(f"Total Income:  {income:.2f}")
        print(f"Total Expense: {expense:.2f}")
        print(f"Net Balance:   {balance:.2f}")
        print("===============================")

    #  Category breakdown
    def category_breakdown(self):
        transactions = self._get_transactions()
        if not transactions:
            print(" No transactions found.")
            return

        categories = defaultdict(lambda: {"income": 0, "expense": 0})
        for t in transactions:
            categories[t["category"]][t["type"]] += t["amount"]

        print("\n===  CATEGORY BREAKDOWN ===")
        for category, data in categories.items():
            print(f"{category}: Income = {data['income']:.2f}, Expense = {data['expense']:.2f}")
        print("=============================")

    #  Spending trends
    def spending_trends(self):
        transactions = self._get_transactions()
        if not transactions:
            print(" No transactions found.")
            return

        # Group by month
        monthly_expense = defaultdict(float)
        for t in transactions:
            month = t["date"][:7]  # YYYY-MM
            if t["type"] == "expense":
                monthly_expense[month] += t["amount"]

        print("\n===  SPENDING TRENDS (by month) ===")
        for month, total in sorted(monthly_expense.items()):
            print(f"{month}: {total:.2f}")
        print("=====================================")



        