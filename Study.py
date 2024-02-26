from cProfile import label
from cgitb import text
from gc import disable
from sqlite3 import Cursor
from ssl import SSLSession
from struct import pack
import tkinter as tk
from tkinter.tix import COLUMN
from ttkthemes import ThemedTk
import pyodbc
from tkinter import ANCHOR, LEFT, NW, TOP, PhotoImage, ttk
from tkinter import  YES,messagebox
import subprocess
from datetime import datetime, timedelta
import customtkinter
import os,sys,sysconfig
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
import sys


# Get the path to the Tcl library directory

class Form1:
    def __init__(self, root):

        
        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        root = customtkinter.CTk()
        root.title("Study Board")
        root.iconbitmap('Logo.ico')
        

        # Define the on_closing function without the self argument
        def on_closing():
            # You can perform cleanup operations here if needed
            root.destroy()  # Destroy the root window
            sys.exit()

        # Attach the on_closing function to the window close event
        root.protocol("WM_DELETE_WINDOW", on_closing)

        def format_hours_minutes(decimal_hours):
            hours, minutes = divmod(int(decimal_hours * 60), 60)
            return hours
        def minimize_window():
            root.destroy()

        
        def selected_option(choice):
            option = OptionMenu.get()
            print(option)
            if option == "Study":
                load_small_window()
            else:
                open_stats()

        def open_stats():
            minimize_window()
            root = customtkinter.CTk()
            app = Form3(root)
            

                
        def load_small_window():
            

            select_query = "SELECT CourseID  FROM Course WHERE name = ?"
            cursor.execute(select_query,combo_box_2.get())
            ID = cursor.fetchone()[0] 
            
            current_datetime = datetime.now()

            # Get the day of the week as an integer (Mon
            #  is 0 and Sunday is 6)
            current_day_of_week = current_datetime.isoweekday()

            insert_query = "INSERT INTO Sessions (Day, TimeStudied, CourseID) VALUES (?, ?, ?);"
    
            # Execute the insertion query
            cursor.execute( insert_query,current_day_of_week, '00:00:00', ID )

             # Commit the transaction
            conn.commit()

            #  def __init__(self, course_to_be_studied, number_of_sessions, type_of_sessions): 
            Form2(combo_box_2.get(), int(combo_box.get()), combo_box_1.get())
            #button.configure(state="disable")
            
            minimize_window()
            
            
        


        def seconds_to_hms(seconds):
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return "{:02}hr : {:02}min : {:02}sec".format(int(hours), int(minutes), int(seconds))

        


        

        def on_select_combo(choice):
            studycourse = combo_box_2.get()

            # Use parameterized query to avoid SQL injection
            sum_query = "SELECT DateDiff('s', currentHours, weeklyHours) FROM Course WHERE name = ?;"

            cursor.execute(sum_query, (studycourse,))
            time_difference_seconds = cursor.fetchone()[0]
            formatted_duration = seconds_to_hms(time_difference_seconds)
            
            message = f"{formatted_duration} left to study {studycourse}"
            messagebox.showinfo("Message", message)
        

        # Get the directory where the script or executable is located
        if getattr(sys, 'frozen', False):
            # If the script is run as an executable, use sys._MEIPASS
            current_directory = os.path.dirname(sys.executable)
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


        # Set the window size
        window_width = 400
        window_height = 550


        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = ((screen_height - window_height) // 2) - 30

        # Set the window size and position
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        
        frame = customtkinter.CTkFrame(root, width=10000, height=600)
        frame.grid_columnconfigure(0, weight=1)
        frame.pack(pady=50)    

        label_2 = customtkinter.CTkLabel(frame ,text="Enter session number",font=("Helvetica", 12,"bold"),fg_color="#424242",corner_radius= 7)
        label_2.pack(pady=20)

        # Create a Combobox with options 1 to 12
        self.number_of_sessions = tk.StringVar()
        options = [str(i) for i in range(1, 13)]
        combo_box = customtkinter.CTkComboBox(frame, values=options,corner_radius= 30 )
        combo_box.set(options[3])  # Set default value
        combo_box.pack(pady=10)

        label_3 = customtkinter.CTkLabel(frame , text="Choose session type", font=("Helvetica", 12,"bold"),fg_color="#424242",corner_radius= 7)
        label_3.pack(pady=20)
        options = ['01hr:30min', '01hr:00min', '00hr:50min']

        combo_box_1 = customtkinter.CTkComboBox(frame, values=options,corner_radius= 30)
        combo_box_1.set(options[2])  # Set default value
        combo_box_1.pack(pady=10)

        label_3_1 = customtkinter.CTkLabel(frame ,text="Choose study course", font=("Helvetica", 12, "bold"),fg_color="#424242",corner_radius= 7)
        label_3_1.pack(pady=20)
        
        combo_box_2 = customtkinter.CTkComboBox(frame, state="normal",corner_radius= 30)
        combo_box_2.pack(pady=20,padx = 50)

        cursor.execute("SELECT name FROM Course WHERE Format(weeklyHours, 'hh:nn:ss am/pm') <> Format(currentHours, 'hh:nn:ss am/pm');")
        names = cursor.fetchall()
        
        options =  [[item[0] for item in names]]
        combo_box_2.configure(values=[item[0] for item in names],command=on_select_combo)


        OptionMenu = customtkinter.CTkOptionMenu(root,values=[],command=selected_option)
        OptionMenu.pack()

        if not options or not options[0]:
            message_text = "You have no courses to study, you're done for the week"
            messagebox.showinfo("Message", message_text)
            OptionMenu.configure(values=["Stats"])
            OptionMenu.set("Stats")
            combo_box_2.set("¯\_(ツ)_/¯")
            combo_box_1.configure(values=[])
            combo_box_1.set("¯\_(ツ)_/¯")
            combo_box.configure(values=[])
            combo_box.set("¯\_(ツ)_/¯")

        else :
            OptionMenu.configure(values=["Study","Stats"])    
            combo_box_2.set(options[0][0]) 
            OptionMenu.set("Study")

        root.mainloop()
        
      
        

       
        


class Form2: 
    def __init__(self, course_to_be_studied, number_of_sessions, type_of_sessions):
        #customtkinter.set_appearance_mode("dark")
        #customtkinter.set_default_color_theme("green")


        self.rooter=tk.Toplevel()
        # Set the window size and position
        window_width = 170
        window_height = 150
        x_coordinate = self.rooter.winfo_screenwidth() - window_width
        y_coordinate = 0

        def open_new_studydashboard():
            self.rooter.destroy()
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("green")
            root = customtkinter.CTk()
            root.title("Study Board")
            app = Form1(root)
            root.iconbitmap('Logo.ico')
            sys.exit()
            


        self.rooter.protocol("WM_DELETE_WINDOW", open_new_studydashboard)

        
        # Set the window size and position
        self.rooter.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        
        #self.rooter.geometry("300x200+100+100")
        self.rooter.title("Timer")
        self.rooter.iconbitmap('Logo.ico')
        self.rooter.configure(background="#373737")
             
        def on_combobox_selected(choice):
        # Update self.course when Combobox selection changes
            selected_value = self.combo_box_2.get()
            self.course = selected_value
            print(self.course)
            print(self.combo_box_2)


            select_query = "SELECT CourseID  FROM Course WHERE name = ?"
            self.cursor.execute(select_query,self.course)
            ID = self.cursor.fetchone()[0] 
            


            current_datetime = datetime.now()

            # Get the day of the week as an integer (Monday is 1 and Sunday is 7)
            current_day_of_week = current_datetime.isoweekday()

            insert_query = "INSERT INTO Sessions (Day, TimeStudied, CourseID) VALUES (?, ?, ?);"
    
            # Execute the insertion query
            self.cursor.execute( insert_query,current_day_of_week, '00:00:00', ID )

             # Commit the transaction
            self.conn.commit()


        
        # Get the directory where the script or executable is located
        if getattr(sys, 'frozen', False):
            # If the script is run as an executable, use sys._MEIPASS
            current_directory = os.path.dirname(sys.executable)
        else:
            # If the script is run as a script, use the script's directory
            current_directory = os.path.dirname(os.path.abspath(__file__))

        # Combine the current directory with the database file name
        db_file_path = os.path.join(current_directory, 'CourseInfo.accdb')

        # Construct the connection string
        self.conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_file_path};'

        try:
            # Connect to the database
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            print("Connected to the database.")
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            raise  # Re-raise the exception to see the full traceback
        

        self.rooter.iconbitmap('Logo.ico')
        self.rooter.wm_attributes("-topmost", 1)
        self.rooter.overrideredirect(True)

        img = ImageTk.PhotoImage(Image.open("exit.png").resize((20, 20)))

        topFrame = customtkinter.CTkFrame(self.rooter, width=150, height=50, fg_color="#373737")
        topFrame.pack(side=tk.TOP, fill=tk.X, expand=1, anchor=tk.N)

        frame_2 = customtkinter.CTkFrame(topFrame, corner_radius=0, fg_color="#373737", width=30, height=30)
        frame_2.grid(row=0, column=0, padx=8, sticky="NW")

        frame1 = customtkinter.CTkFrame(topFrame, corner_radius=0, fg_color="#373737", width=30, height=30)
        frame1.grid(row=0, column=1)

        frame_3 = customtkinter.CTkFrame(topFrame, corner_radius=0, fg_color="#373737", width=30, height=30)
        frame_3.grid(row=0, column=2)

        exit_button = customtkinter.CTkButton(frame_2, text="", image=img, height=20, width=20, compound="top", fg_color="#373737", hover_color="#4a4a4a", corner_radius=5, command=open_new_studydashboard)
        exit_button.grid(row=0, column=0)  # Add horizontal padding to the right of the button

        self.sessions = number_of_sessions
        self.label = customtkinter.CTkLabel(frame1, text=f"Session 1/{self.sessions}", font=("Helvetica", 10),fg_color="#212120",corner_radius= 7)
        self.label.pack()

        self.label_2 = customtkinter.CTkLabel(self.rooter, font=("ds-digital", 18,"bold"))
        self.label_2.pack(pady=0)

        label_3 = customtkinter.CTkLabel(self.rooter, text="Time left", font=("Helvetica", 10))
        label_3.pack(pady=2)

        self.label_4 = customtkinter.CTkLabel(self.rooter, font=("Helvetica", 10))
        self.label_4.pack(pady=0)

        combo_var = tk.StringVar()
        self.combo_box_2 = customtkinter.CTkComboBox(self.rooter, variable=combo_var, state="normal", command=on_combobox_selected)
        self.combo_box_2.pack(pady=0)

        # Fetch names from the database
        self.cursor.execute("SELECT name FROM Course WHERE Format(weeklyHours, 'hh:nn:ss am/pm') <> Format(currentHours, 'hh:nn:ss am/pm');")
        names = self.cursor.fetchall()

        #self.rooter.mainloop.overrideredirect(True)

        # Extract names and update Combobox values
        updated_values = [name[0] for name in names]
        self.combo_box_2.configure(values=[name[0] for name in names])

        # Set default value if it exists in the list
        self.course = course_to_be_studied

        def set_default_value():
            if self.course in updated_values:
                self.combo_box_2.set(self.course)

        # Print for debugging
        
        set_default_value()

       
       

        if type_of_sessions == '01hr:30min':
            self.session_seconds = 5400
        elif type_of_sessions == '01hr:00min':
            self.session_seconds = 3600
        else:
            self.session_seconds = 3000
            # self.session_seconds = 10  # SHOULD REMOVE THIS#

        
       

        self.current_session = 1
        self.time_remaining = timedelta(seconds=self.session_seconds)
        self.is_break = False

        self.update_display()

        

    def seconds_to_hms(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}hr : {:02}min : {:02}sec".format(int(hours), int(minutes), int(seconds))

        
    def update_display(self):
        if not self.is_break: 

            select_query = "SELECT DateDiff('s', currentHours,weeklyhours) FROM Course WHERE name = ?;"

            # Execute the query
            self.cursor.execute(select_query, self.course)
            diff_seconds = self.cursor.fetchone()[0]

            if (diff_seconds == 0):
                self.cursor.execute("SELECT name FROM Course WHERE Format(weeklyHours, 'hh:nn:ss am/pm') <> Format(currentHours, 'hh:nn:ss am/pm');")
                names_result = self.cursor.fetchall()
                self.label_2.configure(text='↻')
                if not names_result:
                        
                        self.label_2.configure(text="Weekly hours done!")
                        self.label_4.configure(text="00hr : 00min: 00sec")
                        message_text = "Done for the week!"
                        messagebox.showinfo("Jubilation", message_text)
                        return
                else:
                    self.label_4.configure(text="00hr : 00min: 00sec")
                    list = [row[0] for row in names_result]
                    self.combo_box_2.configure(values=[row[0] for row in names_result])
                    self.course = list[0]
                    self.rooter.after(0, self.course)

                    #=======================================================================================================================================================

                    select_query = "SELECT CourseID  FROM Course WHERE name = ?"
                    self.cursor.execute(select_query,self.course)
                    ID = self.cursor.fetchone()[0] 
                    


                    current_datetime = datetime.now()

                    # Get the day of the week as an integer (Monday is 1 and Sunday is 7)
                    current_day_of_week = current_datetime.isoweekday()

                    insert_query = "INSERT INTO Sessions (Day, TimeStudied, CourseID) VALUES (?, ?, ?);"
            
                    # Execute the insertion query
                    self.cursor.execute( insert_query,current_day_of_week, '00:00:00', ID )

                    # Commit the transaction
                    self.conn.commit()

                    #=======================================================================================================================================================

                    self.combo_box_2.set(self.course)
                    message_text = f"You've finished the prev course, now you can study {self.course}"
                    messagebox.showinfo("Message", message_text)
                

            hours_left = self.seconds_to_hms(diff_seconds)
            self.label_4.configure(text=hours_left)

        time_str = str(self.time_remaining).split(".")[0]
        self.label_2.configure(text=time_str)
        self.rooter.after(1000, self.update_timer)

    def update_timer(self):
        if self.time_remaining.total_seconds() > 0:
            if not self.is_break:
                ##########################################################
                update_query = f"UPDATE Course SET currentHours = DateAdd('s', 1, currentHours) WHERE name = ?;"
                self.cursor.execute(update_query, self.course)
                self.conn.commit()

                select_query = "SELECT MAX(SessionID) FROM Sessions;"
                self.cursor.execute(select_query)
                SessionID = self.cursor.fetchone()[0]
                #print(SessionID)

                update_query = f"UPDATE Sessions SET TimeStudied = DateAdd('s', 1, TimeStudied) WHERE SessionID = ?;"
                self.cursor.execute(update_query, SessionID)
                self.conn.commit()


                ##########################################################
            self.time_remaining -= timedelta(seconds=1)
            self.update_display()
        else:
            if self.current_session < self.sessions:
                self.is_break = not self.is_break
                if self.is_break:
                    self.label.configure(text="Study Break")
                    self.time_remaining = timedelta(seconds=600)
                    # self.time_remaining = timedelta(seconds=5)    # SHOULD REMOVE THIS#
                    
                else:
                    self.current_session += 1
                    self.label.configure(text=f"Session {self.current_session}/{self.sessions}")
                    self.time_remaining = timedelta(seconds=self.session_seconds)
                    

                self.update_display()
            else:
                self.label_2.configure(text="Completed!")
                
                

    def start_timer(self):
        self.current_session = 1
        self.time_remaining = timedelta(seconds=self.session_seconds)
        self.update_display()



class Form3:
    def __init__(self,root):
        
        # Get the directory where the script or executable is located
        if getattr(sys, 'frozen', False):
            # If the script is run as an executable, use sys._MEIPASS
            current_directory = os.path.dirname(sys.executable)
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

        print(time_studied_dict)
        # time_studied_dict = {'CSC3002F': [1.9, 3.5, 1.5, 3.0, 5.3, 5.3, 0.0], 'INF3011F': [2.5, 0.0, 4.0, 3.7, 1.0, 3.5, 5.6], 'INF3014F': [0.9, 2.0, 1.0, 2.1, 0.7, 0.0, 3.4]}

        # Use the object-oriented approach for plotting
        plt.style.use('ggplot')
        plt.style.use("dark_background")

        
        PURPLE_shades = ["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC", "#7B4FA8", "#8265CC", "#A47CC6", "#7F5491", "#704A8B", "#8B68C1", "#8D72C6", "#63436B", "#A284C0"]
        #PURPLE_shades  = ["#c86558", "#b04238", "#cbd6e4", "#d7e1ee", "#a4a2a8", "#bfcbdb", "#991f17", "#b3bfd1", "#df8879"]
        #PURPLE_shades = ["#b04238", "#cbd6e4", "#a4a2a8", "#bfcbdb", "#d7e1ee", "#c86558", "#b3bfd1", "#991f17", "#df8879"]
        PURPLE_shades = ["#4C2A85", "#FF7F0E", "#2CA02C", "#1F77B4", "#FFDC00", 
          "#9467BD", "#D62728", "#8C564B", "#E377C2", "#7F7F7F", 
          "#BCBD22", "#17BECF"]
        
        PURPLE_shades = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']



        plt.rcParams["axes.prop_cycle"] = plt.cycler(color=[PURPLE_shades[x % len(PURPLE_shades)] for x in range(len(time_studied_dict))])

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

        def on_closing():
            root.destroy()
            sys.exit()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        

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
            
            if time == 0 or current_day_of_week == 1:
                
                print("==========================================================+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=======================")
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
        
        def selected_option(choice):
                    option = OptionMenu.get()
                                
                    if option == "Study":
                        
                        minimize_window()
                        customtkinter.set_appearance_mode("dark")
                        customtkinter.set_default_color_theme("green")
                        root = customtkinter.CTk()
                        root.title("Study Board")
                        root.iconbitmap('Logo.ico')
                        app = Form1(root)
                        

                    elif (option == "Dashboard"):

                        minimize_window()
                        root = customtkinter.CTk()
                        app = Form4(root)




        OptionMenu = customtkinter.CTkOptionMenu(root,values=["Dashboard", "Study"],command=selected_option)
        OptionMenu.pack()
        root.mainloop()



class Form4:
    def __init__(self,root):
        def open_studyBoard():
            minimize_window()
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("green")
            root = customtkinter.CTk()
            root.title("Study Board")
            root.iconbitmap('Logo.ico')
            app = Form1(root)
            

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
            current_datetime = datetime.now()

            # Get the day of the week as an integer (Monday is 1 and Sunday is 7)
            current_day_of_week = current_datetime.isoweekday()
            slider.configure(state="normal")
            selected_value = combo_var.get()
            slider_default()
            label_2_1_1.configure(text=f"{int(slider.get())} hours")
            

            if current_day_of_week == 1:
                
                button.configure(state="normal")

            else:
                
                slider.configure(state="disabled")

            
            
                
            
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
            entry.delete(0, 'end')

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
            current_directory = os.path.dirname(sys.executable)
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

        def on_closing():
            root.destroy()
            sys.exit()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        

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
        root.mainloop()

        

















"""customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.title("Study Board")
app = Form1(root)
root.iconbitmap('Logo.ico')"""