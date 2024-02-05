import tkinter as tk
import subprocess
from tkinter import messagebox

class StudyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home")
        self.iconbitmap('C:\\Users\\Talent Dev\\Desktop\\python-studyInc\\Logo.ico')
        self.setup_window()

    def setup_window(self):
        # Set the window size
        window_width = 300
        window_height = 200

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set the window size and position
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Create buttons in the small window
        dashboard_button = tk.Button(self, text="Dashboard", command=self.open_dashboard)
        dashboard_button.pack(pady=20)

        study_button = tk.Button(self, text="Study", command=self.open_study)
        study_button.pack(pady=20)

    def open_dashboard(self):
        self.run_script("C:\\Users\\Talent Dev\\Desktop\\python-studyInc\\Dashboard.py")

    def open_study(self):
        self.run_script("C:\\Users\\Talent Dev\\Desktop\\python-studyInc\\Study.py")

    def run_script(self, script_path):
        subprocess.Popen(["python", script_path])
        self.destroy()

if __name__ == "__main__":
    app = StudyApp()
    app.mainloop()
