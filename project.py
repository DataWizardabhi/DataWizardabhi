import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Connect to the database
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Create tables with additional fields
cursor.execute('''
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY,
    date TEXT,
    source TEXT,
    description TEXT,
    amount REAL,
    payment_method TEXT,
    currency TEXT,
    notes TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    description TEXT,
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
        self.root.geometry("500x600")
        self.root.configure(bg="Moccasin")  # Set background color to white

        style = ttk.Style() 
        style.configure('TFrame', background='Moccasin') 
        style.configure('TButton', font=('Helvetica',25), padding=20) 
        style.configure('TLabel',  font=('Helvetica', 25))

        # Dashboard
        self.dashboard_frame = ttk.Frame(root, padding="30")
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.dashboard_frame, text="Welcome to Personal Finance Manager", font=("Helvetica", 30)).pack(pady=30)

        self.income_button = ttk.Button(self.dashboard_frame, text="Add Income", command=self.add_income)
        self.income_button.pack(pady=10)

        self.expense_button = ttk.Button(self.dashboard_frame, text="Add Expense", command=self.add_expense)
        self.expense_button.pack(pady=10)

        self.report_button = ttk.Button(self.dashboard_frame, text="View Reports", command=self.view_reports)
        self.report_button.pack(pady=10)

    def add_income(self):
        self.clear_frame()
        self.income_frame = ttk.Frame(self.root, padding="25")
        self.income_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.income_frame, text="Add Income", font=("Helvetica", 26), background='white').pack(pady=50)

        ttk.Label(self.income_frame, text="Date:", background='white').pack()
        self.income_date_entry = ttk.Entry(self.income_frame)
        self.income_date_entry.pack()

        ttk.Label(self.income_frame, text="Source:", background='white').pack()
        self.income_source_entry = ttk.Entry(self.income_frame)
        self.income_source_entry.pack()

        ttk.Label(self.income_frame, text="Description:", background='white').pack()
        self.income_description_entry = ttk.Entry(self.income_frame)
        self.income_description_entry.pack()

        ttk.Label(self.income_frame, text="Amount:", background='white').pack()
        self.income_amount_entry = ttk.Entry(self.income_frame)
        self.income_amount_entry.pack()

        ttk.Label(self.income_frame, text="Payment Method:", background='white').pack()
        self.income_payment_method_entry = ttk.Entry(self.income_frame)
        self.income_payment_method_entry.pack()

        ttk.Label(self.income_frame, text="Currency:", background='white').pack()
        self.income_currency_entry = ttk.Entry(self.income_frame)
        self.income_currency_entry.pack()

        ttk.Label(self.income_frame, text="Notes:", background='white').pack()
        self.income_notes_entry = ttk.Entry(self.income_frame)
        self.income_notes_entry.pack()

        ttk.Button(self.income_frame, text="Add", command=self.save_income).pack(pady=5)
        ttk.Button(self.income_frame, text="Back", command=self.show_dashboard).pack(pady=5)

    def save_income(self):
        date = self.income_date_entry.get()
        source = self.income_source_entry.get()
        description = self.income_description_entry.get()
        try:
            amount = float(self.income_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return
        payment_method = self.income_payment_method_entry.get()
        currency = self.income_currency_entry.get()
        notes = self.income_notes_entry.get()

        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO income (date, source, description, amount, payment_method, currency, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (date, source, description, amount, payment_method, currency, notes))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Income added successfully!")
        self.show_dashboard()

    def add_expense(self):
        self.clear_frame()
        self.expense_frame = ttk.Frame(self.root, padding="30")
        self.expense_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.expense_frame, text="Add Expense", font=("Helvetica", 25), background='white').pack(pady=10)

        ttk.Label(self.expense_frame, text="Date:", background='white').pack()
        self.expense_date_entry = ttk.Entry(self.expense_frame)
        self.expense_date_entry.pack()

        ttk.Label(self.expense_frame, text="Category:", background='white').pack()
        self.expense_category_entry = ttk.Entry(self.expense_frame)
        self.expense_category_entry.pack()

        ttk.Label(self.expense_frame, text="Description:", background='white').pack()
        self.expense_description_entry = ttk.Entry(self.expense_frame)
        self.expense_description_entry.pack()

        ttk.Label(self.expense_frame, text="Amount:", background='white').pack()
        self.expense_amount_entry = ttk.Entry(self.expense_frame)
        self.expense_amount_entry.pack()

        ttk.Label(self.expense_frame, text="Payment Method:", background='white').pack()
        self.expense_payment_method_entry = ttk.Entry(self.expense_frame)
        self.expense_payment_method_entry.pack()

        ttk.Label(self.expense_frame, text="Currency:", background='white').pack()
        self.expense_currency_entry = ttk.Entry(self.expense_frame)
        self.expense_currency_entry.pack()

        ttk.Label(self.expense_frame, text="Notes:", background='white').pack()
        self.expense_notes_entry = ttk.Entry(self.expense_frame)
        self.expense_notes_entry.pack()

        ttk.Button(self.expense_frame, text="Add", command=self.save_expense).pack(pady=5)
        ttk.Button(self.expense_frame, text="Back", command=self.show_dashboard).pack(pady=5)

    def save_expense(self):
        date = self.expense_date_entry.get()
        category = self.expense_category_entry.get()
        description = self.expense_description_entry.get()
        try:
            amount = float(self.expense_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return
        payment_method = self.expense_payment_method_entry.get()
        currency = self.expense_currency_entry.get()
        notes = self.expense_notes_entry.get()

        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, category, description, amount, payment_method, currency, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (date, category, description, amount, payment_method, currency, notes))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Expense added successfully!")
        self.show_dashboard()

    def view_reports(self):
        self.clear_frame()
        self.report_frame = ttk.Frame(self.root, padding="10")
        self.report_frame.pack(fill=tk.BOTH, expand=True)

        # Fetch income and expenses data from the database
        conn = sqlite3.connect('finance_manager.db')
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM income")
        total_income = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0.0

        conn.close()

        # Display the report
        ttk.Label(self.report_frame, text=f"Total Income: {total_income:.2f}", background='white').pack(pady=5)
        ttk.Label(self.report_frame, text=f"Total Expenses: {total_expenses:.2f}", background='white').pack(pady=5)
        ttk.Label(self.report_frame, text=f"Net Savings: {total_income - total_expenses:.2f}", background='white').pack(pady=5)

        ttk.Button(self.report_frame, text="Back", command=self.show_dashboard).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_frame()
        self.__init__(self.root)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManagerApp(root)
    root.mainloop()

