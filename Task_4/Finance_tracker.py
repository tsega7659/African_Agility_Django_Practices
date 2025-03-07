import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Main Application Class
class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("600x400")

        # Temporary storage for transactions
        self.transactions = []

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Category:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Type:").grid(row=3, column=0, padx=10, pady=10)

        # Entry Fields
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=0, column=1, padx=10, pady=10)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)

        # Type Dropdown (Income/Expense)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.root, textvariable=self.type_var, values=["Income", "Expense"])
        self.type_dropdown.grid(row=3, column=1, padx=10, pady=10)
        self.type_dropdown.current(0)

        # Buttons
        tk.Button(self.root, text="Add Transaction", command=self.add_transaction).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Delete Transaction", command=self.delete_transaction).grid(row=5, column=0, columnspan=2, pady=10)

        # Transaction List (Treeview)
        self.transaction_tree = ttk.Treeview(self.root, columns=("Category", "Amount", "Date", "Type"), show="headings")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Type", text="Type")
        self.transaction_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Apply soft colors to columns
        self.transaction_tree.tag_configure("Category", background="#E0F7FA")  # Light Cyan
        self.transaction_tree.tag_configure("Amount", background="#FFF3E0")   # Light Orange
        self.transaction_tree.tag_configure("Date", background="#FCE4EC")     # Light Pink
        self.transaction_tree.tag_configure("Type", background="#E8F5E9")     # Light Green

        # Summary Labels
        self.summary_label = tk.Label(self.root, text="Total Income: $0 | Total Expenses: $0 | Balance: $0", font=("Arial", 12))
        self.summary_label.grid(row=7, column=0, columnspan=2, pady=10)

        # Category Filter
        tk.Label(self.root, text="Filter by Category:").grid(row=8, column=0, padx=10, pady=10)
        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(self.root, textvariable=self.filter_var)
        self.filter_dropdown.grid(row=8, column=1, padx=10, pady=10)
        self.filter_dropdown.bind("<<ComboboxSelected>>", self.filter_transactions)

        # Load initial data
        self.update_summary()
        self.update_filter_dropdown()

    def add_transaction(self):
        # Get input values
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        transaction_type = self.type_var.get()

        # Input validation
        if not category or not amount or not date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        # Add transaction to list
        self.transactions.append({
            "category": category,
            "amount": amount,
            "date": date,
            "type": transaction_type
        })

        # Clear input fields
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

        # Update UI
        self.update_transaction_tree()
        self.update_summary()
        self.update_filter_dropdown()

    def delete_transaction(self):
        selected_item = self.transaction_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No transaction selected.")
            return

        # Remove transaction from list
        item_index = self.transaction_tree.index(selected_item)
        del self.transactions[item_index]

        # Update UI
        self.update_transaction_tree()
        self.update_summary()
        self.update_filter_dropdown()

    def update_transaction_tree(self):
        # Clear existing data
        for row in self.transaction_tree.get_children():
            self.transaction_tree.delete(row)

        # Add transactions to Treeview with alternating row colors
        for i, transaction in enumerate(self.transactions):
            tags = ("Category", "Amount", "Date", "Type")
            if i % 2 == 0:
                tags = ("Category", "Amount", "Date", "Type")
            self.transaction_tree.insert("", tk.END, values=(
                transaction["category"],
                f"${transaction['amount']:.2f}",
                transaction["date"],
                transaction["type"]
            ), tags=tags)

    def update_summary(self):
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
        total_expenses = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")
        balance = total_income - total_expenses

        self.summary_label.config(text=f"Total Income: ${total_income:.2f} | Total Expenses: ${total_expenses:.2f} | Balance: ${balance:.2f}")

    def update_filter_dropdown(self):
        categories = list(set(t["category"] for t in self.transactions))
        self.filter_dropdown["values"] = categories

    def filter_transactions(self, event):
        selected_category = self.filter_var.get()
        if selected_category:
            filtered_transactions = [t for t in self.transactions if t["category"] == selected_category]
            self.transaction_tree.delete(*self.transaction_tree.get_children())
            for transaction in filtered_transactions:
                self.transaction_tree.insert("", tk.END, values=(
                    transaction["category"],
                    f"${transaction['amount']:.2f}",
                    transaction["date"],
                    transaction["type"]
                ))
        else:
            self.update_transaction_tree()

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()