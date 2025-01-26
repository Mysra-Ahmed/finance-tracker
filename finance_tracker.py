import sqlite3
import tkinter as tk
from tkinter import messagebox
conn = sqlite3.connect('finance_tracker.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             username TEXT NOT NULL,
             password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS transactions (
             id INTEGER PRIMARY KEY,
             user_id INTEGER,
             type TEXT NOT NULL,
             category TEXT NOT NULL,
             amount REAL NOT NULL,
             date TEXT NOT NULL,
             FOREIGN KEY(user_id) REFERENCES users(id))''')

conn.commit()
conn.close()

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        self.conn = sqlite3.connect('finance_tracker.db')
        self.c = self.conn.cursor()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.login_screen()

    def login_screen(self):
        tk.Label(self.root, text="Username").pack()
        tk.Entry(self.root, textvariable=self.username).pack()
        tk.Label(self.root, text="Password").pack()
        tk.Entry(self.root, textvariable=self.password, show='*').pack()
        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Register", command=self.register).pack()

    def login(self):
        self.c.execute("SELECT * FROM users WHERE username=? AND password=?", (self.username.get(), self.password.get()))
        user = self.c.fetchone()

        if user:
            self.user_id = user[0]
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        self.c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username.get(), self.password.get()))
        self.conn.commit()
        messagebox.showinfo("Success", "Registration successful")

    def main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Personal Finance Tracker").pack()
        tk.Button(self.root, text="Add Transaction", command=self.add_transaction_screen).pack()
        tk.Button(self.root, text="View Transactions", command=self.view_transactions).pack()

    def add_transaction_screen(self):
        self.transaction_type = tk.StringVar()
        self.category = tk.StringVar()
        self.amount = tk.DoubleVar()
        self.date = tk.StringVar()

        tk.Label(self.root, text="Type (Income/Expense)").pack()
        tk.Entry(self.root, textvariable=self.transaction_type).pack()
        tk.Label(self.root, text="Category").pack()
        tk.Entry(self.root, textvariable=self.category).pack()
        tk.Label(self.root, text="Amount").pack()
        tk.Entry(self.root, textvariable=self.amount).pack()
        tk.Label(self.root, text="Date (YYYY-MM-DD)").pack()
        tk.Entry(self.root, textvariable=self.date).pack()
        tk.Button(self.root, text="Add", command=self.add_transaction).pack()

    def add_transaction(self):
        self.c.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                       (self.user_id, self.transaction_type.get(), self.category.get(), self.amount.get(), self.date.get()))
        self.conn.commit()
        messagebox.showinfo("Success", "Transaction added")

    def view_transactions(self):
        self.c.execute("SELECT * FROM transactions WHERE user_id=?", (self.user_id,))
        transactions = self.c.fetchall()

        for widget in self.root.winfo_children():
            widget.destroy()

        for transaction in transactions:
            tk.Label(self.root, text=f"{transaction[2]} - {transaction[3]}: {transaction[4]} on {transaction[5]}").pack()

        tk.Button(self.root, text="Back", command=self.main_screen).pack()

    def __del__(self):
        self.conn.close()

root = tk.Tk()
app = FinanceTracker(root)
root.mainloop()
