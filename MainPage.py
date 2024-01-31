import tkinter as tk
from RegistrationPage import StudentRegistration
from AttendancePage import ViewAttendance
from AttendanceTaking import AttendanceTaking
from Face_Recognition import FaceRecognition
from Face_Detect import FaceDetection
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime as local_datetime

class LectureAttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lecture Attendance Tracking System")
        self.geometry("1081x654")
        self.configure(bg='yellow')  # Set the background color
        self.img = Image.open("GUI picture.png")
        self.img = ImageTk.PhotoImage(self.img)
        background_label = tk.Label(self, image=self.img)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(
            self,
            bg=None,  # Transparent background (R, G, B, A)
            height=654,
            width=1081,
            bd=0,
            highlightthickness=0,
            relief="flat"  # No relief style
        )
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.canvas.pack()

        # Create buttons with raised relief style
        self.create_button("Add Student", self.on_button_click_1, (871.0, 150.0, 141.0, 51.0))
        self.create_button("View Attendance", self.on_button_click_2, (869.0, 232.0, 141.0, 51.0))
        self.create_button("Take Attendance", self.on_button_click_3, (865.0, 318.0, 141.0, 51.0))
        self.create_button("Face Recognition", self.on_button_click_4, (865.0, 411.0, 141.0, 51.0))
        self.create_button("Face Detection", self.on_button_click_5, (865.0, 497.0, 141.0, 51.0))
        
        self.canvas.create_text(
            60.0,
            201.0,
            anchor="nw",
            text="Lecture Attendance\nTracking System",
            fill="white",  # Text color set to white
            font=("Rockwell", 65, "italic")
        )
        self.time_text = self.canvas.create_text(
            856.0,
            62.0,
            anchor="nw",
            text="",
            fill="white",  # Text color set to white
            font=("TimesNewRomanPS BoldMT", 15, "bold")
        )
        self.update_clock()  # Initialize the clock

        # Disable window resizing
        self.resizable(False, False)

    def create_button(self, text, command, coordinates):
        x, y, width, height = coordinates
        button = tk.Button(
            self,
            text=text,
            bg="white",  # Grey background color
            fg="Black",  # Text color set to white
            borderwidth=3,  # Increased border width
            relief="raised",  # Raised relief style
            padx=20,
            pady=10,
            font=("Arial", 12, "bold"),
            command=command
        )
        button.place(x=x, y=y, width=width, height=height, bordermode="outside")
        
    def update_clock(self):
        current_time = local_datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        self.canvas.itemconfigure(self.time_text, text=current_time)
        self.after(1000, self.update_clock)  # Update every second
        
    def on_button_click_1(self):
        self.withdraw()  # Hide the mqqain page
        student_app = StudentRegistration(self,self.img)
        student_app.mainloop()

    def on_button_click_2(self):
        self.withdraw()  # Hide the main page
        student_app = ViewAttendance(self,self.img)
        student_app.mainloop()

    def on_button_click_3(self):
        Attendance = AttendanceTaking()
        Attendance.take_attendance_random_intervals()

    def on_button_click_4(self):
        self.withdraw()
        face_recognition = FaceRecognition()
        face_recognition.recognize_people_from_image()
        self.deiconify()
        
    def on_button_click_5(self):
        self.withdraw()
        face_detect = FaceDetection()
        face_detect.detect_faces_show_confidence()
        self.deiconify()
    
if __name__ == "__main__":
    app = LectureAttendanceApp()
    app.mainloop()

