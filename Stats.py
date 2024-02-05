import os
import pyodbc
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import subprocess
from datetime import datetime
import sys



# Get the directory where the script or executable is located
if getattr(sys, 'frozen', False):
    # If the script is run as an executable, use sys._MEIPASS
    current_directory = sys._MEIPASS
else:
    # If the script is run as a script, use the script's directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Combine the current directory with the database file name
db_file_path = os.path.join(current_directory, 'CourseInfo.accdb')

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

sql_statement = 'SELECT DISTINCT c.name FROM Course AS c INNER JOIN Sessions AS s ON c.CourseID = s.CourseID;'
cursor.execute(sql_statement)
cousrses = cursor.fetchall()
course_list = [item[0] for item in cousrses ]
days = ['Mon', 'Tue', 'Wen', "Thu", 'Fri', 'Sat', 'Sun']
time_studied_dict = {course: [0 for i in range(1,8)] for course in course_list}

for c in time_studied_dict.keys():
    for t in range(0,7):
        sql_statement= "SELECT IIF(SUM(DateDiff('s', '00:00:00', s.TimeStudied)) IS NULL, 0, SUM(DateDiff('s', '00:00:00', s.TimeStudied))) AS TotalTimeInSeconds FROM Sessions AS s INNER JOIN Course AS c ON c.CourseID = s.CourseID WHERE s.day = ? AND c.name = ? ;"   
        cursor.execute(sql_statement,t + 1,c)
        value = cursor.fetchone()[0]
        int(value)
        time_studied_dict[c][t] = round(value/60/60, 2)

print(course_list)
# time_studied_dict = {'CSC3002F': [1.9, 3.5, 1.5, 3.0, 5.3, 5.3, 0.0], 'INF3011F': [2.5, 0.0, 4.0, 3.7, 1.0, 3.5, 5.6], 'INF3014F': [0.9, 2.0, 1.0, 2.1, 0.7, 0.0, 3.4]}

# Use the object-oriented approach for plotting
plt.style.use('ggplot')
plt.style.use("dark_background")


fig, ax = plt.subplots()

arrays = list(time_studied_dict.values())

# Sum arrays from the first key to the second last key
bottom_array = np.sum(arrays[:len(arrays)-1], axis=0)
bottom_array = bottom_array.tolist()

for s in time_studied_dict.keys():
 
    if s != course_list[0] and s != course_list[-1]:

        arr = list(time_studied_dict.values())     
        key_index = course_list.index(s)
        b_array = np.sum(arr[:key_index], axis=0)
        b_array = b_array.tolist()
        ax.bar(days,time_studied_dict[s],bottom=b_array, label=s)

    elif s == course_list[0] :
        ax.bar(days,time_studied_dict[s], label=s)

    elif s == course_list[-1]:
        ax.bar(days,time_studied_dict[s],bottom=bottom_array, label=s)


ax.set_xlabel('Days')
ax.set_ylabel('Hours studied')
ax.set_title('Studying this week')
ax.legend()
#plt.show()



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()

# Set the window size
window_width = 500
window_height = 700

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = ((screen_height - window_height) // 2) - 30

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.title("Stats")
root.iconbitmap('Logo.ico')





# Create a Tkinter frame and embed the Matplotlib figure


frame = customtkinter.CTkFrame(root)
frame.pack()
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack()


frame_2 = customtkinter.CTkFrame(root,corner_radius= 7)
frame_2.pack ( padx = 5, pady= 10)

label_1 = customtkinter.CTkLabel(frame_2, text="Current Streak : 2 weeks",font=("Helvetica", 12,"bold"),fg_color="#000000",corner_radius= 7);
label_1.grid(sticky='NW',padx= 15,pady=20)

label_2 = customtkinter.CTkLabel(frame_2, text="Total time left : 18hr 20min ",font=("Helvetica", 12,"bold"),fg_color="#000000",corner_radius= 7);
label_2.grid(column=1,row=0, padx=20)

label_3 = customtkinter.CTkLabel(frame_2, text="Running avg : 4hr 20min ",font=("Helvetica", 12,"bold"),fg_color="#000000",corner_radius= 7);
label_3.grid(sticky='SW',padx= 15,pady=30)

label_4 = customtkinter.CTkLabel(frame_2, text="Onward avg : 4hr 20min ",font=("Helvetica", 12,"bold"),fg_color="#000000",corner_radius= 7);
label_4.grid(column=1,row=1, padx=20)

def streak():

    # Open and read the content of the file
    with open('streak.txt', 'r') as file:
        content = file.read()

    # Check if the content is a single digit
    if content.isdigit() and len(content) == 1:
        # Convert the content to an integer
        digit_value = int(content)
        
    if digit_value == 1:
         label_1.configure(text=f"Current Streak : {digit_value} week")
    else:
        label_1.configure(text=f"Current Streak : {digit_value} weeks")

def seconds_to_hr_min(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}hr {:02}min".format(int(hours), int(minutes))

def time_left():
     sql_statement = "SELECT SUM(DateDiff('s', currentHours, weeklyHours)) FROM Course;"
     cursor.execute(sql_statement)
     time = seconds_to_hr_min(cursor.fetchone()[0])

     label_2.configure(text=f"Total time left : {time} ")

def avg_studied():

    current_datetime = datetime.now()

    # Get the day of the week as an integer (Monday is 1 and Sunday is 7)
    current_day_of_week = current_datetime.isoweekday()

    sql_statement = "SELECT IIF(SUM(IIF(day < ?, DateDiff('s', '00:00:00', TimeStudied), 0)) IS NULL, 0, SUM(IIF(day < ?, DateDiff('s', '00:00:00', TimeStudied), 0))) AS TotalTimeStudied FROM Sessions;"
    cursor.execute(sql_statement,current_day_of_week,current_day_of_week)
    time = cursor.fetchone()[0] 
    
    if time == 0:
         
        label_3.configure(text=f"Running avg : 00hr 00min ")
         
    else:
        x = seconds_to_hr_min(int(time/(current_day_of_week - 1 )))
        label_3.configure(text=f"Running avg : {x} ")

def onward_avg():
     
    current_datetime = datetime.now()

    # Get the day of the week as an integer (Monday is 1 and Sunday is 7)
    days_left = 8 - (current_datetime.isoweekday() + 1)


    sql_statement="SELECT SUM(DateDiff('s', currentHours, weeklyHours)) FROM Course ;"
    cursor.execute(sql_statement)
    time = cursor.fetchone()[0]
    #time = 136800
    
    if days_left == 0:

        x = seconds_to_hr_min(int(time))
        label_4.configure(text=f"Crunch time : {x} ")
    
    else:
        x = seconds_to_hr_min(int(time / days_left))
        label_4.configure(text=f"Onward avg : {x} ")

    
     

    
    


streak()
time_left()
avg_studied()
onward_avg()



def minimize_window():
    root.destroy()

def run_Stats():
    root.mainloop()

def selected_option(choice):
            option = OptionMenu.get()
                        
            if option == "Study":
                
                study_script_path = "Study.py"
                subprocess.Popen(["python", study_script_path])
                minimize_window()

            elif (option == "Dashboard"):

                dashboard_script_path = "Dashboard.py"
                subprocess.Popen(["python", dashboard_script_path])
                minimize_window()




OptionMenu = customtkinter.CTkOptionMenu(root,values=["Dashboard", "Study"],command=selected_option)
OptionMenu.pack()

#root.mainloop()