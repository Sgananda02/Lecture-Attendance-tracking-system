import tkinter as tk
from tkinter import messagebox
from StudentRegister import StudentRegister  # Import the StudentRegister class


class StudentRegistration(tk.Toplevel):
    def __init__(self, main_app, image_reference):
        super().__init__(main_app)
        self.title("Student Information System")
        self.geometry("1081x654")
        self.configure(bg="#FFFFFF")
        self.photo = None
        self.main_app = main_app
        self.image_reference = image_reference 
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # Create the canvas
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=654,
            width=1081,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Labels for text entry fields
        label_1 = tk.Label(
            self,
            text="Student Number:",
            bg="#FFFFFF",
            font=("Arial", 12, "bold"),
        )
        label_1.place(x=48.0, y=100.0)

        self.number_entry = tk.Entry(
            self,
            bd=2,  # Increased border width
            bg="white",  # Background color
            fg="#000716",
            relief="sunken",  # Sunken relief style
            font=("Arial", 12),
        )
        self.number_entry.place(x=48.0, y=130.0, width=174.0, height=36.0)

        label_2 = tk.Label(
            self,
            text="Name:",
            bg="#FFFFFF",
            font=("Arial", 12, "bold"),
        )
        label_2.place(x=48.0, y=195.0)

        self.name_entry = tk.Entry(
            self,
            bd=2,
            bg="white",
            fg="#000716",
            relief="sunken",
            font=("Arial", 12),
        )
        self.name_entry.place(x=48.0, y=225.0, width=174.0, height=36.0)

        label_3 = tk.Label(
            self,
            text="Surname:",
            bg="#FFFFFF",
            font=("Arial", 12, "bold"),
        )
        label_3.place(x=48.0, y=290.0)

        self.surname_entry = tk.Entry(
            self,
            bd=2,
            bg="white",
            fg="#000716",
            relief="sunken",
            font=("Arial", 12),
        )
        self.surname_entry.place(x=48.0, y=320.0, width=174.0, height=36.0)

        self.image_label = tk.Label(
            self,
            bg="white",
            bd=2,
            relief="sunken",
            font=("Arial", 12),
        )
        self.image_label.place(x=348.0, y=60.0, width=698.0, height=491.0)

        # Create buttons with grey background and rounded corners (border radius)
        button_1 = tk.Button(
            self,
            text="Register",
            command=lambda: self.on_button_click(),
            bg="#CCCCCC",
            fg="black",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            padx=20,
            pady=10,
            font=("Arial", 12, "bold"),
        )
        button_1.place(x=479.0, y=587.0, width=156.0, height=51.0, bordermode="outside")
        # Disable window resizing
        self.resizable(False, False)
     
    def on_button_click(self):
        student_number = self.number_entry.get()
        student_name = self.name_entry.get()
        student_surname = self.surname_entry.get()

        # Validate inputs
        if not student_number or not student_name or not student_surname:
            messagebox.showerror("Error", "All fields must be filled.")
            return
        
        self.withdraw()
        register = StudentRegister()
        register.capture_faces(student_name, student_surname, student_number)
        messagebox.showinfo("Success", "Registration was successful!")
        self.number_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.surname_entry.delete(0, "end")
        self.deiconify()
           
    def on_close(self):
        self.destroy()
        self.main_app.deiconify()
