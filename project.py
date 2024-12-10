import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# Database setup
def setup_database():
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()

    # Drop old tables if they exist to avoid conflicts
    cursor.execute("DROP TABLE IF EXISTS income")
    cursor.execute("DROP TABLE IF EXISTS expenses")

    # Create tables with only the needed fields
    cursor.execute('''
    CREATE TABLE income (
        id INTEGER PRIMARY KEY,
        date TEXT,
        source TEXT,
        amount REAL,
        payment_method TEXT,
        currency TEXT,
        notes TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        amount REAL,
        payment_method TEXT,
        currency TEXT,
        notes TEXT
    )
    ''')

    conn.commit()
    conn.close()


class FinanceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("600x700")
        self.root.configure(bg="Wheat")

        # Configure the button style
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 30))  # Set button font size

        self.show_dashboard()

    def show_dashboard(self):
        self.clear_frame()
        dashboard_frame = ttk.Frame(self.root, padding="20")
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(dashboard_frame, text="Welcome to Personal Finance Manager", font=("Helvetica", 40)).pack(pady=20)

        ttk.Button(dashboard_frame, text="Add Income", command=self.add_income, width=30).pack(pady=10)
        ttk.Button(dashboard_frame, text="Add Expense", command=self.add_expense, width=30).pack(pady=10)
        ttk.Button(dashboard_frame, text="View Reports", command=self.view_reports, width=30).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_income(self):
        self.show_form("Add Income", self.save_income, [
            ("Date", "date"),
            ("Source", "source"),
            ("Amount", "amount"),
            ("Payment Method", "payment_method"),
            ("Currency", "currency"),
            ("Notes", "notes")
        ])

    def add_expense(self):
        self.show_form("Add Expense", self.save_expense, [
            ("Date", "date"),
            ("Category", "category"),
            ("Amount", "amount"),
            ("Payment Method", "payment_method"),
            ("Currency", "currency"),
            ("Notes", "notes")
        ])

    def show_form(self, title, save_command, fields):
        self.clear_frame()
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text=title, font=("Helvetica", 18)).pack(pady=10)

        self.form_entries = {}

        for label, key in fields:
            # Adjusted label size for better visibility
            ttk.Label(form_frame, text=f"{label}:", font=("Helvetica", 12), background="#f0f8ff").pack()
            entry = ttk.Entry(form_frame, width=50)  # Increased the entry width for better input
            entry.pack(pady=5)
            self.form_entries[key] = entry

        ttk.Button(form_frame, text="Save", command=save_command, width=30).pack(pady=15)
        ttk.Button(form_frame, text="Back", command=self.show_dashboard, width=30).pack(pady=5)

    def save_income(self):
        self.save_record("income", [
            "date", "source", "amount", "payment_method", "currency", "notes"
        ])

    def save_expense(self):
        self.save_record("expenses", [
            "date", "category", "amount", "payment_method", "currency", "notes"
        ])

    def save_record(self, table, fields):
        values = []
        for field in fields:
            entry = self.form_entries[field].get()
            if field == "amount":
                try:
                    entry = float(entry)
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount. Please enter a number.")
                    return
            values.append(entry)

        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()

        try:
            cursor.execute(f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(['?'] * len(fields))})", values)
            conn.commit()
            messagebox.showinfo("Success", f"{table[:-1].capitalize()} added successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

        self.show_dashboard()

    def view_reports(self):
        self.clear_frame()
        report_frame = ttk.Frame(self.root, padding="200")
        report_frame.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM income")
        total_income = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0.0

        conn.close()

        ttk.Label(report_frame, text=f"Total Income: {total_income:.2f}", font=("Helvetica", 25)).pack(pady=10)
        ttk.Label(report_frame, text=f"Total Expenses: {total_expenses:.2f}", font=("Helvetica", 25)).pack(pady=10)
        ttk.Label(report_frame, text=f"Net Savings: {total_income - total_expenses:.2f}", font=("Helvetica", 25)).pack(pady=10)

        ttk.Button(report_frame, text="Back", command=self.show_dashboard, width=30).pack(pady=15)


if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = FinanceManagerApp(root)
    root.mainloop()
