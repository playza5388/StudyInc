import tkinter as tk
from tkinter import messagebox

class Form1:
    def __init__(self, root):
        self.root = root
        self.root.title("Form 1")

        self.variable_to_transfer = tk.StringVar()

        label = tk.Label(root, text="Enter information:")
        label.pack()

        entry = tk.Entry(root, textvariable=self.variable_to_transfer)
        entry.pack()

        button = tk.Button(root, text="Submit", command=self.close_and_open_form2)
        button.pack()

    def close_and_open_form2(self):
        # Close Form1
        self.root.destroy()

        # Open Form2 and pass the information
        Form2(self.variable_to_transfer.get())

class Form2:
    def __init__(self, transferred_info):
        self.root = tk.Tk()
        self.root.title("Form 2")

        label = tk.Label(self.root, text=f"Received Information: {transferred_info}")
        label.pack()

        self.root.mainloop()

# Create Form1
root = tk.Tk()
app = Form1(root)
root.mainloop()
