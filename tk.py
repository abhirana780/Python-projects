import tkinter as tk
from tkinter import messagebox
import pandas as pd


class BankAccount:
    def __init__(self, account_number, account_holder, pin, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.pin = pin  # PIN should be stored as a string
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance


class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking System")

        self.accounts = {}
        
        tk.Label(root, text="Account Number").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Account Holder Name").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="PIN").grid(row=2, column=0, padx=10, pady=5)

        self.account_number_entry = tk.Entry(root)
        self.account_holder_entry = tk.Entry(root)
        self.pin_entry = tk.Entry(root, show="*")

        self.account_number_entry.grid(row=0, column=1, padx=10, pady=5)
        self.account_holder_entry.grid(row=1, column=1, padx=10, pady=5)
        self.pin_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(root, text="Create Account", command=self.create_account).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Label(root, text="Account Actions").grid(row=4, column=0, columnspan=2, pady=10)
        tk.Label(root, text="Amount").grid(row=5, column=0, padx=10, pady=5)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(root, text="Deposit", command=self.deposit).grid(row=6, column=0, pady=10)
        tk.Button(root, text="Withdraw", command=self.withdraw).grid(row=6, column=1, pady=10)
        tk.Button(root, text="Check Balance", command=self.check_balance).grid(row=7, column=0, columnspan=2, pady=10)

        self.load_accounts()  # Load accounts on app start

    def save_accounts(self):
        # This is for saving accounts to a CSV
        data = {
            'account_number': [],
            'account_holder': [],
            'pin': [],
            'balance': []
        }
        for account in self.accounts.values():
            data['account_number'].append(account.account_number)
            data['account_holder'].append(account.account_holder)
            data['pin'].append(account.pin.strip())  # Store PIN as a stripped string
            data['balance'].append(account.get_balance())

        df = pd.DataFrame(data)
        df.to_csv("accounts.csv", index=False)

    def load_accounts(self):
        # Load accounts from the CSV file
        try:
            df = pd.read_csv("accounts.csv")
            for _, row in df.iterrows():
                account_number = row['account_number']
                account_holder = row['account_holder']
                pin = str(row['pin']).strip()  # Ensure PIN is stripped of extra spaces
                balance = row['balance']
                self.accounts[account_number] = BankAccount(account_number, account_holder, pin, balance)
        except FileNotFoundError:
            pass  # If no file exists, just proceed without loading any accounts

    def verify_pin(self, account_number, pin):
        # Strip entered PIN of any extra spaces and ensure both are strings
        if account_number in self.accounts and str(self.accounts[account_number].pin).strip() == str(pin).strip():
            return True
        return False

    def create_account(self):
        account_number = self.account_number_entry.get()
        account_holder = self.account_holder_entry.get()
        pin = str(self.pin_entry.get()).strip()  # Strip extra spaces when creating account

        if account_number and account_holder and pin:
            if account_number not in self.accounts:
                self.accounts[account_number] = BankAccount(account_number, account_holder, pin)
                self.save_accounts()
                messagebox.showinfo("Success", "Account created successfully!")
            else:
                messagebox.showerror("Error", "Account number already exists!")
        else:
            messagebox.showerror("Error", "Please enter all fields!")

    def deposit(self):
        account_number = self.account_number_entry.get()
        pin = self.pin_entry.get()
        amount = self.amount_entry.get()

        if self.verify_pin(account_number, pin):
            try:
                amount = float(amount)
                if self.accounts[account_number].deposit(amount):
                    self.save_accounts()
                    messagebox.showinfo("Success", "Amount deposited successfully!")
                else:
                    messagebox.showerror("Error", "Invalid amount!")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number!")
        else:
            messagebox.showerror("Error", "Invalid account or PIN!")

    def withdraw(self):
        account_number = self.account_number_entry.get()
        pin = self.pin_entry.get()
        amount = self.amount_entry.get()

        if self.verify_pin(account_number, pin):
            try:
                amount = float(amount)
                if self.accounts[account_number].withdraw(amount):
                    self.save_accounts()
                    messagebox.showinfo("Success", "Amount withdrawn successfully!")
                else:
                    messagebox.showerror("Error", "Insufficient balance!")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number!")
        else:
            messagebox.showerror("Error", "Invalid account or PIN!")

    def check_balance(self):
        account_number = self.account_number_entry.get()
        pin = self.pin_entry.get()
        if self.verify_pin(account_number, pin):
            balance = self.accounts[account_number].get_balance()
            messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")
        else:
            messagebox.showerror("Error", "Invalid account or PIN!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
