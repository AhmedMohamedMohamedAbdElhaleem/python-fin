import datetime
import uuid

class TransactionManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    # Add new transaction
    def add_transaction(self):
        if not self.user_manager.current_user:
            print(" Please login first.")
            return

        t_type = input("Enter type (income/expense): ").strip().lower()
        if t_type not in ["income", "expense"]:
            print(" Invalid type.")
            return

        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print(" Invalid amount.")
            return

        category = input("Enter category (e.g. Food, Salary, Rent): ").strip()
        note = input("Enter note (optional): ").strip()
        date_str = input("Enter date (YYYY-MM-DD) or leave empty for today: ").strip()
        date = date_str if date_str else datetime.date.today().isoformat()

        transaction = {
            "id": str(uuid.uuid4()), 
            "type": t_type,
            "amount": amount,
            "category": category,
            "note": note,
            "date": date
        }

        self.user_manager.current_user["transactions"].append(transaction)
        # self.user_manager.save_users()
        
        self.user_manager.save()  # Save after adding transaction


        print(f" {t_type.capitalize()} added successfully!")

    # View all transactions
    def view_transactions(self):
        if not self.user_manager.current_user:
            print(" Please login first.")
            return

        transactions = self.user_manager.current_user["transactions"]
        if not transactions:
            print(" No transactions found.")
            return

        print(f"\n Transactions for {self.user_manager.current_user['username']}:")
        print("-" * 60)
        for i, t in enumerate(transactions, start=1):
            print(f"{i}. [{t['type'].upper()}] {t['amount']} | {t['category']} | {t['date']} | {t['note']}")
        print("-" * 60)

    # Edit transaction
    def edit_transaction(self):
        if not self.user_manager.current_user:
            print(" Please login first.")
            return

        transactions = self.user_manager.current_user["transactions"]
        if not transactions:
            print(" No transactions to edit.")
            return

        self.view_transactions()
        choice = input("Enter transaction number to edit: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(transactions)):
            print(" Invalid choice.")
            return

        index = int(choice) - 1
        transaction = transactions[index]

        print("\n--- Edit Transaction ---")
        print("Press Enter to keep current value.")
        new_type = input(f"Type ({transaction['type']}): ").strip().lower()
        new_amount = input(f"Amount ({transaction['amount']}): ").strip()
        new_category = input(f"Category ({transaction['category']}): ").strip()
        new_note = input(f"Note ({transaction['note']}): ").strip()
        new_date = input(f"Date ({transaction['date']}): ").strip()

        if new_type in ["income", "expense"]:
            transaction["type"] = new_type
        if new_amount:
            try:
                transaction["amount"] = float(new_amount)
            except ValueError:
                print(" Invalid amount, keeping old value.")
        if new_category:
            transaction["category"] = new_category
        if new_note:
            transaction["note"] = new_note
        if new_date:
            transaction["date"] = new_date

        # self.user_manager.save_users()

        self.user_manager.save()  # Save after editing transaction


        print("Transaction updated successfully!")

    # Delete transaction with confirmation
    def delete_transaction(self):
        if not self.user_manager.current_user:
            print(" Please login first.")
            return

        transactions = self.user_manager.current_user["transactions"]
        if not transactions:
            print(" No transactions to delete.")
            return

        self.view_transactions()
        choice = input("Enter transaction number to delete: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(transactions)):
            print(" Invalid choice.")
            return

        index = int(choice) - 1
        t = transactions[index]

        confirm = input(f" Are you sure you want to delete '{t['category']}' ({t['amount']})? (y/n): ").strip().lower()
        if confirm == "y":
            del transactions[index]
            # self.user_manager.save_users()

            self.user_manager.save()  # Save after deleting transaction



            print("Transaction deleted successfully.")
        else:
            print(" Deletion cancelled.")


