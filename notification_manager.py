from datetime import datetime
from decimal import Decimal


class NotificationManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def check_notifications(self):
        """Check and show notifications like overspending or nearing goals."""
        user = self.user_manager.current_user
        if not user:
            print("Please login first.")
            return

        notifications = []

        # Check monthly budget
        budgets = user.get("monthly_budgets", [])
        transactions = user.get("transactions", [])
        for b in budgets:
            month = b["month"]
            budget = Decimal(b["amount"])
            total_spent = Decimal("0")
            for t in transactions:
                if t.get("type") == "expense" and t.get("date", "").startswith(month):
                    total_spent += Decimal(t.get("amount", "0"))
            if total_spent >= budget * Decimal("0.9"):
                notifications.append(
                    f"⚠️ You're close to your budget limit for {month} ({total_spent:.2f}/{budget:.2f})"
                )

        # Check savings goals
        goals = user.get("savings_goals", [])
        for g in goals:
            target = Decimal(g["target_amount"])
            saved = Decimal(g.get("saved_amount", "0"))  # ✅ هنا التعديل
            if saved >= target:
                notifications.append(f"🎉 Goal '{g['name']}' achieved!")
            elif saved >= target * Decimal("0.8"):
                notifications.append(
            f"💰 You're close to achieving your goal '{g['name']}' ({saved:.2f}/{target:.2f})"
        )

        if notifications:
            print("\n=== Notifications ===")
            for n in notifications:
                print("-", n)
        else:
            print("No notifications right now.")
