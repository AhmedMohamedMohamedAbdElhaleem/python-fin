
import uuid
from decimal import Decimal, InvalidOperation
from datetime import datetime

class SavingsGoalManager:
    """
    Manage savings goals for the current user.
    Stores goals inside user dict under 'savings_goals'.
    Each goal:
      {
        "id": "<uuid>",
        "name": "Buy Laptop",
        "target_amount": "1500.00",   # stored as string for JSON safety (we convert to Decimal)
        "saved_amount": "200.00",
        "deadline": "2025-12-31" or "",
        "created_at": "2025-10-24T21:00:00"
      }
    """
    def __init__(self, user_manager):
        self.user_manager = user_manager

    # ---------- helpers ----------
    def _now_iso(self):
        return datetime.now().isoformat()

    def _to_decimal(self, value):
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return Decimal("0")

    def _ensure_goals_list(self):
        """Ensure current user has 'savings_goals' list to avoid KeyError."""
        u = self.user_manager.current_user
        if u is None:
            return False
        if "savings_goals" not in u:
            u["savings_goals"] = []
        return True

    def _save_users(self):
        """Proxy save to UserManager."""
        self.user_manager.save()

    # ---------- CRUD operations ----------
    def add_goal(self):
        """Add a new savings goal."""
        if not self._ensure_goals_list():
            print("Please login first.")
            return

        name = input("Goal name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        amt = input("Target amount: ").strip()
        try:
            target = self._to_decimal(amt)
            if target <= 0:
                print("Target must be greater than 0.")
                return
        except Exception:
            print("Invalid amount.")
            return

        deadline = input("Deadline (YYYY-MM-DD) [optional]: ").strip()
        # optional validation
        if deadline:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                print("Invalid deadline format. Use YYYY-MM-DD or leave empty.")
                return

        goal = {
            "id": str(uuid.uuid4()),
            "name": name,
            "target_amount": str(target),   # store as string for JSON safety
            "saved_amount": "0",            # start at 0
            "deadline": deadline,
            "created_at": self._now_iso()
        }

        self.user_manager.current_user["savings_goals"].append(goal)
        self._save_users()
        print(f"Goal '{name}' added (target {target:.2f}).")

    def view_goals(self):
        """List all goals with progress."""
        if not self._ensure_goals_list():
            print("Please login first.")
            return

        goals = self.user_manager.current_user.get("savings_goals", [])
        if not goals:
            print("No savings goals found.")
            return

        print("\n=== Savings Goals ===")
        for i, g in enumerate(goals, start=1):
            target = self._to_decimal(g.get("target_amount", "0"))
            saved = self._to_decimal(g.get("saved_amount", "0"))
            pct = (saved / target * 100) if target > 0 else Decimal("0")
            status = "✅ Reached" if saved >= target else "🔸 In progress"
            deadline = f" | deadline: {g['deadline']}" if g.get("deadline") else ""
            print(f"{i}. {g['name']} -- saved: {saved:.2f} / {target:.2f} ({pct:.1f}%) {status}{deadline}")
        print("=====================\n")

    def delete_goal(self):
        """Delete a goal by index."""
        if not self._ensure_goals_list():
            print("Please login first.")
            return

        goals = self.user_manager.current_user.get("savings_goals", [])
        if not goals:
            print("No goals to delete.")
            return

        self.view_goals()
        choice = input("Enter goal number to delete: ").strip()
        if not choice.isdigit():
            print("Invalid input.")
            return
        idx = int(choice) - 1
        if idx < 0 or idx >= len(goals):
            print("Invalid number.")
            return

        g = goals.pop(idx)
        self._save_users()
        print(f"Deleted goal '{g['name']}'.")

    def add_saved_amount(self):
        """
        Allocate amount to a goal.
        This will:
         - create an expense transaction with category 'Savings' and note referencing the goal
         - increment goal.saved_amount
        """
        if not self._ensure_goals_list():
            print("Please login first.")
            return

        goals = self.user_manager.current_user.get("savings_goals", [])
        if not goals:
            print("No goals found.")
            return

        self.view_goals()
        choice = input("Choose goal number to allocate to: ").strip()
        if not choice.isdigit():
            print("Invalid input.")
            return
        idx = int(choice) - 1
        if idx < 0 or idx >= len(goals):
            print("Invalid number.")
            return

        amt_str = input("Amount to allocate: ").strip()
        try:
            amt = self._to_decimal(amt_str)
            if amt <= 0:
                print("Amount must be positive.")
                return
        except Exception:
            print("Invalid amount.")
            return

        # create transaction via TransactionManager style but we don't import it here.
        # We'll add a simple transaction dict and append to user's transactions:
        transaction = {
            "id": str(uuid.uuid4()),
            "type": "expense",
            "amount": float(amt),   # existing system stores amounts as floats
            "category": "Savings",
            "note": f"Allocated to goal {goals[idx]['id']} - {goals[idx]['name']}",
            "date": datetime.now().date().isoformat()
        }

        # append transaction and increment saved_amount
        self.user_manager.current_user.setdefault("transactions", []).append(transaction)

        # update saved_amount (store as string)
        existing_saved = self._to_decimal(goals[idx].get("saved_amount", "0"))
        goals[idx]["saved_amount"] = str(existing_saved + amt)

        self._save_users()
        print(f"Allocated {amt:.2f} to goal '{goals[idx]['name']}'. Transaction recorded.")

    def edit_goal(self):
        """Edit name/target/deadline of a goal."""
        if not self._ensure_goals_list():
            print("Please login first.")
            return

        goals = self.user_manager.current_user.get("savings_goals", [])
        if not goals:
            print("No goals found.")
            return

        self.view_goals()
        choice = input("Choose goal number to edit: ").strip()
        if not choice.isdigit():
            print("Invalid input.")
            return
        idx = int(choice) - 1
        if idx < 0 or idx >= len(goals):
            print("Invalid number.")
            return

        g = goals[idx]
        print("Press Enter to keep current value.")
        new_name = input(f"Name ({g['name']}): ").strip()
        new_target = input(f"Target ({g['target_amount']}): ").strip()
        new_deadline = input(f"Deadline ({g.get('deadline','')}) [YYYY-MM-DD]: ").strip()

        if new_name:
            g['name'] = new_name
        if new_target:
            try:
                t = self._to_decimal(new_target)
                if t > 0:
                    g['target_amount'] = str(t)
                else:
                    print("Target must be > 0. Keeping old.")
            except Exception:
                print("Invalid target. Keeping old.")
        if new_deadline:
            try:
                datetime.strptime(new_deadline, "%Y-%m-%d")
                g['deadline'] = new_deadline
            except ValueError:
                print("Invalid date format. Keeping old.")

        self._save_users()
        print("Goal updated.")
