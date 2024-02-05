import tkinter as tk
from PIL import Image, ImageTk
import customtkinter

class Form3:
    def __init__(self, root):
        self.root = root
        self.root.title('')
        self.root.config(background="#373737")
        self.root.geometry("180x150")

        img = ImageTk.PhotoImage(Image.open("exit.png").resize((20, 20)))

        topFrame = customtkinter.CTkFrame(self.root, width=150, height=50, fg_color="#373737")
        topFrame.pack(side=tk.TOP, fill=tk.X, expand=1, anchor=tk.N)

        frame_2 = customtkinter.CTkFrame(topFrame, corner_radius=0, fg_color="#373737", width=30, height=30)
        frame_2.grid(row=0, column=0, padx=15, sticky="NW")

        frame1 = customtkinter.CTkFrame(topFrame, corner_radius=0, fg_color="#373737", width=30, height=30)
        frame1.grid(row=0, column=1)

        frame_3 = customtkinter.CTkFrame(topFrame, corner_radius=0, fg_color="#373737", width=30, height=30)
        frame_3.grid(row=0, column=2)

        exit_button = customtkinter.CTkButton(frame_2, text="", image=img, height=20, width=20, compound="top", fg_color="#373737", hover_color="#4a4a4a", corner_radius=5, command=self.close_window)
        exit_button.grid(row=0, column=0)  # Add horizontal padding to the right of the button

        label = customtkinter.CTkLabel(frame1, text=f"Study Break", font=("Helvetica", 10))
        label.pack()                                    

        label_2 = customtkinter.CTkLabel(self.root, font=("ds-digital", 18, "bold"))
        label_2.pack(pady=0)

        label_3 = customtkinter.CTkLabel(self.root, text="Time left", font=("Helvetica", 10))
        label_3.pack(pady=2)

        label_4 = customtkinter.CTkLabel(self.root, font=("Helvetica", 10))
        label_4.pack(pady=0)

        combo_var = tk.StringVar()
        combo_box_2 = customtkinter.CTkComboBox(self.root, variable=combo_var)
        combo_box_2.pack(pady=0)

        self.root.overrideredirect(True)

    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Form3(root)
    root.mainloop()
