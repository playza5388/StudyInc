from logging import root
import customtkinter
from tokenize import Whitespace
from turtle import color, ondrag
from ttkthemes import ThemedTk
from datetime import datetime, timedelta
from tkinter import YES, messagebox
from tkinter import ttk
import pyodbc
import subprocess
import os,sys
import Study



def open_studyBoard():
    minimize_window()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root = customtkinter.CTk()
    root.title("Study Board")
    app = Study.Form1(root)
    root.iconbitmap('Logo.ico')
    root.mainloop()

def greeting():
    current_time = datetime.now()
    current_hour = current_time.hour

    if (0 <= current_hour < 12):
        return "Good morning Babalwe"
    elif (12 <= current_hour < 18):
        return "Good afternoon Babalwe" 
    else:
        return "Good evening Babalwe"
    
    
def hours_to_datetime(hours):
    # Create a datetime object with the given number of hours
    time_delta = timedelta(hours=hours)
    base_datetime = datetime(2000, 1, 1)
    result_datetime = base_datetime + time_delta
    return result_datetime

def set_weekly_hours():
     
    weekly_hours = int(slider.get())
    selected_course = combobox.get()
    
    if (weekly_hours == 1):
         message = "You've set up {} hour for {} this week.".format(weekly_hours,selected_course)

    else:
         message = "You've set up {} hours for {} this week.".format(weekly_hours,selected_course)

    messagebox.showinfo("Message", message)

    formatted_time = hours_to_datetime(weekly_hours)

    update_query = f"UPDATE Course SET weeklyHours = ? WHERE name = ?"
    
    cursor.execute(update_query, formatted_time.time(), selected_course)
    conn.commit()
               

def on_select_combo(choice):

    course = combo_box.get()

    result = messagebox.askyesno("Confirmation", "Are you sure you want to delete?")
    if (result==YES):

        reset_query = "DELETE FROM Sessions WHERE CourseID IN (SELECT CourseID FROM Course WHERE name = ?);"
        cursor.execute(reset_query, course)
        conn.commit()


        delete_query = "DELETE FROM Course WHERE name = ?"
        cursor.execute(delete_query, course)

        # Commit the transaction
        conn.commit()

        message = "{} has been deleted.".format(course)
    
    else:
        message = "{} has not been deleted.".format(course)
    
    messagebox.showinfo("Message", message)

def on_select(choice):
    slider.configure(state="normal")
    button.configure(state="normal")
    selected_value = combo_var.get()
    slider_default()
    label_2_1_1.configure(text=f"{int(slider.get())} hours")
    
def on_enter_courses(event):

   
    combobox['values'] = ()

    cursor.execute("SELECT name FROM Course")
    names = cursor.fetchall()
    combobox.configure(values=[item[0] for item in names])

def on_enter(event):

    combo_box['values'] = ()

    cursor.execute("SELECT name FROM Course")
    names = cursor.fetchall()
    combo_box.configure(values=[item[0] for item in names])

    


def AddNewcourse():
    name = entry.get()
    hours = 0
    weeklyHours = hours_to_datetime(hours).time()
    currentHours = hours_to_datetime(hours).time()
    #print(type(weeklyHours))
    
    #query
    insert_query = "INSERT INTO Course (name, weeklyHours, currentHours) VALUES (?, ?, ?)"
    
    # Execute the insertion query
    cursor.execute(insert_query, name, weeklyHours, currentHours)

    # Commit the transaction
    conn.commit()

    message = "{} has been added to the database use slider above to set weekly hours.".format(name)
    messagebox.showinfo("Message", message)
    #entry.delete(0, tk.END)

def minimize_window():
    root.destroy()


def slider_default():
    slider_query = "SELECT HOUR(weeklyHours) FROM Course WHERE name = ?;"
    subject = combobox.get()
    cursor.execute(slider_query, (subject,))
    default_value = cursor.fetchone()[0]
    slider.set(default_value)

def sliding(value):
    label_2_1_1.configure(text=f"{int(value)} hours")
            

#Establishind DB connection

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





# Create the main window using ThemedTk
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.title("Dashboard")
root.iconbitmap('Logo.ico')

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

label_text = greeting()
label = customtkinter.CTkLabel(root, text=label_text, font=("Cooper", 18))
label.pack(pady=10)

label_1 = customtkinter.CTkLabel(root, text="edit course weekly hours", font=("cooper", 14,"bold"),fg_color="#48a388", corner_radius= 30)
label_1.pack(pady=10)

# Create a customtkinter frame
frame = customtkinter.CTkFrame(root, width=10000, height=600)
frame.grid_columnconfigure(0, weight=1)
frame.pack()

# Label
label_2_1 = customtkinter.CTkLabel(frame, text="Select course", font=("Helvetica", 12, "bold"),fg_color="#353536",corner_radius= 7)
label_2_1.grid(row=0, column=0, pady=20)

# Dropdown box (Combobox)
combo_var = customtkinter.StringVar()
combobox = customtkinter.CTkComboBox(frame, variable=combo_var, state="normal",corner_radius= 30,width=150,command=on_select)
combobox.bind("<Enter>", on_enter_courses)
combobox.grid(row=1, column=0, pady=10)

# Slider with a draggable circle handle
slider = customtkinter.CTkSlider(frame, from_=0, to=22, command=sliding)
slider.grid(row=2, column=0, pady=10)
slider.set(0)
slider.configure(state="disabled")

label_2_1_1 = customtkinter.CTkLabel(frame, text=f"{int(slider.get())} hours", font=("Helvetica", 12))
label_2_1_1.grid(row=3, column=0, pady=5)


# Button to trigger an action
button = customtkinter.CTkButton(frame, text="Set Weekly Hours", command=set_weekly_hours)
button.grid(row=4, column=0, pady=30,padx = 50)
button.configure(state="disabled")
# Label to display the result

label_1_1 = customtkinter.CTkLabel(root, text="Insert/delete courses", font=("cooper", 14,"bold"),fg_color="#48a388", corner_radius= 30)
label_1_1.pack(pady=10)

frame_2 = customtkinter.CTkScrollableFrame(root,width=216,height=80)
frame_2.grid_columnconfigure(0, weight=1)
frame_2.pack()


label_2 = customtkinter.CTkLabel(frame_2, text="Add new course name", font=("Helvetica", 12,"bold"),fg_color="#353536",corner_radius= 7)
label_2.pack(pady=20)

entry = customtkinter.CTkEntry(frame_2,width=150)
entry.pack(pady=10)

button_1 = customtkinter.CTkButton(frame_2, text="Add",width=150, command=AddNewcourse)
button_1.pack(pady=10)

label_3 = customtkinter.CTkLabel(frame_2, text="Delete courses", font=("Helvetica", 12,"bold"),fg_color="#353536",corner_radius= 7)
label_3.pack(pady=20)

combo_box = customtkinter.CTkComboBox(frame_2, variable=combo_var, corner_radius= 30,width=150, state="normal", command=on_select_combo)
combo_box.pack(pady=10)

combo_box.bind("<Enter>", on_enter)
# Bind the on_select function to the <<ComboboxSelected>> event

dashboard_button = customtkinter.CTkButton(root, text="Go to studyBoard", command=open_studyBoard)
dashboard_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()


