from datetime import datetime
from decimal import Decimal, InvalidOperation

class MonthlyBudgetManager:


    def __init__(self, user_manager):
        self.user_manager = user_manager

    # Helper
    def _to_decimal(self, value):
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return Decimal("0")

    def _ensure_budgets_list(self):
        """Ensure current user has 'monthly_budgets' list."""
        u = self.user_manager.current_user
        if u is None:
            return False
        if "monthly_budgets" not in u:
            u["monthly_budgets"] = []
        return True

    def _save_users(self):
        self.user_manager.save()

    # Main functions
    def set_budget(self):
        if not self._ensure_budgets_list():
            print("Please login first.")
            return

        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month format. Use YYYY-MM.")
            return

        amount_str = input("Enter budget amount: ").strip()
        try:
            amount = self._to_decimal(amount_str)
            if amount <= 0:
                print("Amount must be positive.")
                return
        except Exception:
            print("Invalid amount.")
            return

        # Update or add budget
        budgets = self.user_manager.current_user["monthly_budgets"]
        for b in budgets:
            if b["month"] == month:
                b["amount"] = str(amount)
                self._save_users()
                print(f"Budget for {month} updated to {amount:.2f}.")
                return

        budgets.append({"month": month, "amount": str(amount)})
        self._save_users()
        print(f"Budget for {month} set to {amount:.2f} successfully!")

    def view_budget_status(self):
        if not self._ensure_budgets_list():
            print("Please login first.")
            return

        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Invalid month format.")
            return

        budgets = self.user_manager.current_user.get("monthly_budgets", [])
        budget_entry = next((b for b in budgets if b["month"] == month), None)
        if not budget_entry:
            print("No budget set for this month.")
            return

        budget = self._to_decimal(budget_entry["amount"])

        # Calculate total expenses in that month
        transactions = self.user_manager.current_user.get("transactions", [])
        total_spent = Decimal("0")
        for t in transactions:
            if t.get("type") == "expense" and t.get("date", "").startswith(month):
                total_spent += self._to_decimal(t.get("amount", "0"))

        remaining = budget - total_spent
        pct_used = (total_spent / budget * Decimal("100")) if budget > 0 else Decimal("0")

        print(f"\n=== Monthly budget for {month} ===")
        print(f"Budget: {budget:.2f}")
        print(f"Spent: {total_spent:.2f}")
        print(f"Remaining: {remaining:.2f}")
        print(f"Percent used: {pct_used:.2f}%")
