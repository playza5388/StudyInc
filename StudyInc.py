import time
import customtkinter
import subprocess
import pyodbc
from datetime import datetime
from tkinter import messagebox
import os
import sys
import sysconfig
import tkinter as tk
import Study


def resource_path(relative_path):
    # https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def minimize_window():
    root.destroy()


def open_dashboard():
    minimize_window()
    root = customtkinter.CTk()
    app = Study.Form4(root)


def open_study():
    minimize_window()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root = customtkinter.CTk()
    root.title("Study Board")
    app = Study.Form1(root)
    root.iconbitmap('Logo.ico')
    root.mainloop()
    


# Get the directory where the script or executable is located
if getattr(sys, 'frozen', False):
    # If the script is run as an executable, use sys._MEIPASS
    current_directory = os.path.dirname(sys.executable)
else:
    # If the script is run as a script, use the script's directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Combine the current directory with the database file name
db_file_path = os.path.join(current_directory, 'CourseInfo.accdb')

# Print the current working directory and the constructed path
print(f"Current Working Directory: {os.getcwd()}")
print(f"Constructed Database Path: {db_file_path}")

# Construct the connection string
conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_file_path};'

try:
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Connected to the database.")
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")
    raise  # Re-raise the exception to see the full traceback

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.title("StudyInc")
root.iconbitmap('Logo.ico')

def on_closing():
        root.destroy()
        sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Set the window size
window_width = 300
window_height = 200

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Create buttons in the small window
dashboard_button = customtkinter.CTkButton(root, text="Dashboard", command=open_dashboard)
dashboard_button.pack(pady=40)

study_button = customtkinter.CTkButton(root, text="Study", command=open_study)
study_button.pack(pady=0)

# Get the current day of the week
day = datetime.now().isoweekday()

# Read the reset flag from the file
reset_flag_file_path = 'reset_flag.txt'

if not day == 1:
    with open(reset_flag_file_path, 'w') as reset_flag_file:
        reset_flag_file.write("0")

try:
    with open(reset_flag_file_path, 'r') as reset_flag_file:
        reset_flag = int(reset_flag_file.readline())
except FileNotFoundError:
    # If the file is not found, assume the reset hasn't occurred yet
    reset_flag = 0

if day == 1 and reset_flag == 0:
    try:
        sql_statement = "SELECT SUM(DateDiff('s', currentHours, weeklyHours)) FROM Course;"
        cursor.execute(sql_statement)
        time_value = cursor.fetchone()[0]

        if time_value == 0:
            message = "You've successfully completed last week's work!! Good luck for this week"
            messagebox.showinfo("Message", message)

            # Update streak.txt
            file_path_streak = 'streak.txt'
            with open(file_path_streak, 'r') as file:
                streak = int(file.readline())
                streak += 1

            with open(file_path_streak, 'w') as file:
                file.write(str(streak))
        else:
            message = "You failed in completing last week's work. Good luck for this week"
            messagebox.showinfo("Message", message)

            file_path_streak = 'streak.txt'
            with open(file_path_streak, 'w') as file:
                file.write("0")

        # Set the reset flag to 1 in the file
        with open(reset_flag_file_path, 'w') as reset_flag_file:
            reset_flag_file.write("1")

        # Update query to set currentHours in Course table
        update_query = "UPDATE Course SET currentHours = '12:00:00am';"
        cursor.execute(update_query)
        conn.commit()

        reset_query = "DELETE FROM Sessions;"
        cursor.execute(reset_query)
        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the Tkinter event loop
root.mainloop()
