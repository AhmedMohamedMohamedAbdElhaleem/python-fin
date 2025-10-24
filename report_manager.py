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


    def spending_trends(self):
        transactions = self._get_transactions()
        if not transactions:
            print(" No transactions found.")
            return


        monthly_expense = defaultdict(float)
        for t in transactions:
            month = t["date"][:7]  
            if t["type"] == "expense":
                monthly_expense[month] += t["amount"]

        print("\n===  SPENDING TRENDS (by month) ===")
        for month, total in sorted(monthly_expense.items()):
            print(f"{month}: {total:.2f}")
        print("=====================================")

    from decimal import Decimal, InvalidOperation

    def ascii_visualization(self):
        """
        Display ASCII-based charts showing:
        1. Income vs Expense comparison bar
        2. Monthly Expense Trend
        """
        transactions = self._get_transactions()
        if not transactions:
            print(" No transactions found.")
            return

        # Helper function to convert safely to Decimal
        def to_dec(value):
            try:
                return Decimal(str(value))
            except (InvalidOperation, ValueError):
                return Decimal("0")

        # --- Income vs Expense Summary ---
        total_income = sum(to_dec(t["amount"]) for t in transactions if t["type"] == "income")
        total_expense = sum(to_dec(t["amount"]) for t in transactions if t["type"] == "expense")

        print("\n=== ASCII VISUALIZATION: Income vs Expense ===")
        bar_width = 40
        max_val = max(total_income, total_expense, Decimal("1"))

        def make_bar(value):
            length = int((value / max_val) * bar_width)
            return "#" * length + " " * (bar_width - length)

        print(f"Income : {make_bar(total_income)} ({total_income:.2f})")
        print(f"Expense: {make_bar(total_expense)} ({total_expense:.2f})")

        # --- Monthly Expense Trend ---
        monthly = {}
        for t in transactions:
            if t["type"] == "expense":
                date = t["date"]
                month = date[:7]  # YYYY-MM
                monthly[month] = monthly.get(month, Decimal("0")) + to_dec(t["amount"])

        if monthly:
            print("\n=== Monthly Expense Trend (YYYY-MM) ===")
            max_month = max(monthly.values()) or Decimal("1")
            for mon, val in sorted(monthly.items()):
                length = int((val / max_month) * 30)
                bar = "*" * length
                print(f"{mon}: {bar} ({val:.2f})")
        else:
            print("\nNo expense transactions to show monthly trend.")

        print("============================================\n")

            # 🔹 ASCII Visualization Feature
    