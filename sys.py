import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import hashlib
import os

# Directory to store CSV files
DATA_DIR = "school_data"
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
USER_FILE = os.path.join(DATA_DIR, "users.csv")
STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")
GRADES_FILE = os.path.join(DATA_DIR, "grades.csv")
TIMETABLE_FILE = os.path.join(DATA_DIR, "timetable.csv")
FEES_FILE = os.path.join(DATA_DIR, "fees.csv")

# Initialize data files if not present
def initialize_file(file_path, columns):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

initialize_file(USER_FILE, ["role", "pin"])
initialize_file(STUDENT_FILE, ["Name", "Class", "Age", "Gender", "Mobile"])
initialize_file(ATTENDANCE_FILE, ["Name", "Date", "Status"])
initialize_file(GRADES_FILE, ["Name", "Subject", "Marks"])
initialize_file(TIMETABLE_FILE, ["Class", "Day", "Timetable"])
initialize_file(FEES_FILE, ["Name", "Amount", "Status"])

# Utility function to hash PIN
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

# Function to verify user credentials
def verify_user(role, pin):
    if os.path.exists(USER_FILE) and os.stat(USER_FILE).st_size > 0:
        users = pd.read_csv(USER_FILE)
        if not users.empty:
            hashed_pin = hash_pin(pin)
            user = users[(users["role"] == role) & (users["pin"] == hashed_pin)]
            return not user.empty
    return False

# Function to create admin account
def create_admin():
    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0 or pd.read_csv(USER_FILE).empty:
        admin_pin = simpledialog.askstring("Create Admin", "Set Admin PIN:", show='*')
        if admin_pin:
            hashed_pin = hash_pin(admin_pin)
            admin_data = pd.DataFrame([{"role": "admin", "pin": hashed_pin}])
            admin_data.to_csv(USER_FILE, index=False)
            messagebox.showinfo("Success", "Admin account created successfully!")
        else:
            messagebox.showerror("Error", "PIN cannot be empty.")
    else:
        messagebox.showinfo("Info", "Admin account already exists.")

# GUI Functions
def login():
    role = role_var.get()
    pin = pin_entry.get()

    if verify_user(role, pin):
        messagebox.showinfo("Success", f"Welcome, {role}!")
        main_window(role)
    else:
        messagebox.showerror("Error", "Invalid credentials.")

# Main window after login
def main_window(role):
    login_window.destroy()
    window = tk.Tk()
    window.title(f"{role.capitalize()} Dashboard")

    if role == "admin":
        tk.Button(window, text="Enroll Student", command=enroll_student).pack(pady=10)
        tk.Button(window, text="Manage Attendance", command=manage_attendance).pack(pady=10)
        tk.Button(window, text="Grade Management", command=manage_grades).pack(pady=10)
        tk.Button(window, text="Timetable Scheduling", command=manage_timetable).pack(pady=10)
        tk.Button(window, text="Fee Management", command=manage_fees).pack(pady=10)
    
    window.mainloop()

# Functions for features
def enroll_student():
    student_name = simpledialog.askstring("Enroll Student", "Enter Student Name:")
    student_class = simpledialog.askstring("Enroll Student", "Enter Student Class:")
    student_age = simpledialog.askinteger("Enroll Student", "Enter Student Age:")
    student_gender = simpledialog.askstring("Enroll Student", "Enter Student Gender:")
    student_mobile = simpledialog.askstring("Enroll Student", "Enter Student Mob.no:")

    if student_name and student_class and student_age and student_gender and student_mobile:
        student_data = pd.DataFrame([{"Name": student_name, "Class": student_class, "Age": student_age, "Gender": student_gender, "Mobile": student_mobile}])
        df = pd.read_csv(STUDENT_FILE)
        df = pd.concat([df, student_data], ignore_index=True)  # Concatenate the new data
        df.to_csv(STUDENT_FILE, index=False)  # Save the updated DataFrame
        messagebox.showinfo("Success", "Student enrolled successfully!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def manage_attendance():
    student_name = simpledialog.askstring("Manage Attendance", "Enter Student Name:")
    attendance_date = simpledialog.askstring("Manage Attendance", "Enter Date (YYYY-MM-DD):")
    attendance_status = simpledialog.askstring("Manage Attendance", "Enter Status (Present/Absent):")

    if student_name and attendance_date and attendance_status:
        attendance_data = pd.DataFrame([{"Name": student_name, "Date": attendance_date, "Status": attendance_status}])
        df = pd.read_csv(ATTENDANCE_FILE)
        df = pd.concat([df, attendance_data], ignore_index=True)  # Concatenate the new data
        df.to_csv(ATTENDANCE_FILE, index=False)  # Save the updated DataFrame
        messagebox.showinfo("Success", "Attendance recorded successfully!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def manage_grades():
    student_name = simpledialog.askstring("Manage Grades", "Enter Student Name:")
    subject = simpledialog.askstring("Manage Grades", "Enter Subject:")
    marks = simpledialog.askinteger("Manage Grades", "Enter Marks:")

    if student_name and subject and marks is not None:
        grades_data = pd.DataFrame([{"Name": student_name, "Subject": subject, "Marks": marks}])
        df = pd.read_csv(GRADES_FILE)
        df = pd.concat([df, grades_data], ignore_index=True)  # Concatenate the new data
        df.to_csv(GRADES_FILE, index=False)  # Save the updated DataFrame
        messagebox.showinfo("Success", "Grade recorded successfully!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def manage_timetable():
    class_name = simpledialog.askstring("Timetable Scheduling", "Enter Class Name:")
    day = simpledialog.askstring("Timetable Scheduling", "Enter Day:")
    timetable = simpledialog.askstring("Timetable Scheduling", "Enter Timetable:")

    if class_name and day and timetable:
        timetable_data = pd.DataFrame([{"Class": class_name, "Day": day, "Timetable": timetable}])
        df = pd.read_csv(TIMETABLE_FILE)
        df = pd.concat([df, timetable_data], ignore_index=True)  # Concatenate the new data
        df.to_csv(TIMETABLE_FILE, index=False)  # Save the updated DataFrame
        messagebox.showinfo("Success", "Timetable updated successfully!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def manage_fees():
    student_name = simpledialog.askstring("Fee Management", "Enter Student Name:")
    fee_amount = simpledialog.askinteger("Fee Management", "Enter Fee Amount:")
    fee_status = simpledialog.askstring("Fee Management", "Enter Fee Status (Paid/Unpaid):")

    if student_name and fee_amount is not None and fee_status:
        fee_data = pd.DataFrame([{"Name": student_name, "Amount": fee_amount, "Status": fee_status}])
        df = pd.read_csv(FEES_FILE)
        df = pd.concat([df, fee_data], ignore_index=True)  # Concatenate the new data
        df.to_csv(FEES_FILE, index=False)  # Save the updated DataFrame
        messagebox.showinfo("Success", "Fee details recorded successfully!")
    else:
        messagebox.showerror("Error", "All fields are required!")


# Login Window
login_window = tk.Tk()
login_window.title("School Management System")

role_var = tk.StringVar(value="admin")

# Role Selection
tk.Label(login_window, text="Select Role:").pack()
tk.Radiobutton(login_window, text="Admin", variable=role_var, value="admin").pack()
tk.Radiobutton(login_window, text="Teacher", variable=role_var, value="teacher").pack()
tk.Radiobutton(login_window, text="Student", variable=role_var, value="student").pack()
tk.Radiobutton(login_window, text="Parent", variable=role_var, value="parent").pack()

# PIN Entry
tk.Label(login_window, text="Enter PIN:").pack()
pin_entry = tk.Entry(login_window, show='*')
pin_entry.pack()
import logging
logger.info(f'Student {student_name} enrolled successfully')
logger.warning(f'All
# Create a logger
logger = logging.getLogger('school_management_system')
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('school_management_system.log')
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Modify the functions to add logs
def initialize_file(file_path, columns):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)
        logger.info(f'Initialized file {file_path}')

def verify_user(role, pin):
    if os.path.exists(USER_FILE) and os.stat(USER_FILE).st_size > 0:
        users = pd.read_csv(USER_FILE)
        if not users.empty:
            hashed_pin = hash_pin(pin)
            user = users[(users["role"] == role) & (users["pin"] == hashed_pin)]
            if not user.empty:
                logger.info(f'User {role} logged in successfully')
                return True
            else:
                logger.warning(f'Invalid credentials for user {role}')
                return False
    logger.warning(f'User file not found or empty')
    return False

def create_admin():
    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0 or pd.read_csv(USER_FILE).empty:
        admin_pin = simpledialog.askstring("Create Admin", "Set Admin PIN:", show='*')
        if admin_pin:
            hashed_pin = hash_pin(admin_pin)
            admin_data = pd.DataFrame([{"role": "admin", "pin": hashed_pin}])
            admin_data.to_csv(USER_FILE, index=False)
            logger.info('Admin account created successfully')
            messagebox.showinfo("Success", "Admin account created successfully!")
        else:
            logger.warning('Admin PIN cannot be empty')
            messagebox.showerror("Error", "PIN cannot be empty.")
    else:
        logger.info('Admin account already exists')
        messagebox.showinfo("Info", "Admin account already exists.")

def login():
    role = role_var.get()
    pin = pin_entry.get()

    if verify_user(role, pin):
        logger.info(f'User {role} logged in successfully')
        messagebox.showinfo("Success", f"Welcome, {role}!")
        main_window(role)
    else:
        logger.warning(f'Invalid credentials for user {role}')
        messagebox.showerror("Error", "Invalid credentials.")

def enroll_student():
    student_name = simpledialog.askstring("Enroll Student", "Enter Student Name:")
    student_class = simpledialog.askstring("Enroll Student", "Enter Student Class:")
    student_age = simpledialog.askinteger("Enroll Student", "Enter Student Age:")
    student_gender = simpledialog.askstring("Enroll Student", "Enter Student Gender:")
    student_mobile = simpledialog.askstring("Enroll Student", "Enter Student Mob.no:")

    if student_name and student_class and student_age and student_gender and student_mobile:
        studentin Button
tk.Button(login_window, text="Login", command=login).pack(pady=10)

# Create Admin Button
tk.Button(login_window, text="Create Admin", command=create_admin).pack(pady=10)

login_window.mainloop()
