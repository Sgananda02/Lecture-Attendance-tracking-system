import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Register import AttendanceAnalyzer

class ViewAttendance(tk.Toplevel):
    def __init__(self, main_app,image_reference ):
        super().__init__(main_app)
        self.geometry("1081x654")
        self.configure(bg="#FFFFFF")
        self.title("View Attendance")
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

        # Module Code Label and Entry
        module_code_label = tk.Label(
            self,
            text="Module Code:",
            bg="#FFFFFF",
            font=("Lalezar Regular", 14, "bold")
        )
        module_code_label.place(x=32.0, y=130.0)
        
        self.entry_1 = tk.Entry(
            self,
            bd=2,
            bg="white",
            fg="#000716",
            relief="sunken",  # Sunken relief style
            font=("Arial", 12),
        )
        self.entry_1.place(x=218.5, y=130.0, width=218.0, height=29.0)

        # Date Label and Entry
        date_label = tk.Label(
            self,
            text="Date (dd/mm/yyyy):",
            bg="#FFFFFF",
            font=("Inter", 14, "bold")
        )
        date_label.place(x=27.0, y=200.0)

        self.entry_2 = tk.Entry(
           self,
            bd=2,
            bg="white",
            fg="#000716",
            relief="sunken",  # Sunken relief style
            font=("Arial", 12),
        )
        self.entry_2.place(x=218.5, y=200.0, width=218.0, height=29.0)

        # Download Button
        button_1 = tk.Button(
            self,
            text="Download",
            command=self.on_button1_click,
            bg="#D9D9D9",
            fg="#000000",
            relief="flat",
            font=("Arial", 12, "bold")
        )
        button_1.place(x=829.0, y=559.0, width=172.0, height=46.0)

        # View Button
        button_2 = tk.Button(
            self,
            text="View",
            command=self.on_button2_click,
            bg="#D9D9D9",
            fg="#000000",
            relief="flat",
            font=("Arial", 12, "bold")
        )
        button_2.place(x=77.0, y=559.0, width=172.0, height=46.0)
        columns =("Student Number", "Attendance Status","Attendance Percent")
       # Create a Table using ttk.Treeview
        self.table = ttk.Treeview(self, columns=columns)
        self.table['show'] = 'headings'
        self.table.heading('Student Number', text="Student Number")
        self.table.heading('Attendance Status', text="Attendance Status")
        self.table.heading('Attendance Percent', text="Attendance Percent")
        self.table.place(x=498.0, y=98.0, width=567.0, height=420.0)
        # Start the main loop
        self.resizable(False, False)

    def on_button1_click(self):
        analyzer = AttendanceAnalyzer()
        course_code = self.entry_1.get()
        Date = self.entry_2.get()
        session_id = analyzer.get_session_id(course_code, Date)
        if session_id:
            attendance_data = analyzer.retrieve_attendance_data(session_id)
            data = analyzer.generate_final_conclusion(attendance_data)
            Final = analyzer.calculate_overall_status(data)
            analyzer.create_pdf(Final, course_code)
            messagebox.showinfo("Success", "Register Downloaded successfully")
        else:
            messagebox.showerror("Error", f"Session not found for course code: {course_code}")

    def on_button2_click(self):
        analyzer = AttendanceAnalyzer()
        course_code = self.entry_1.get()
        Date = self.entry_2.get()
        session_id = analyzer.get_session_id(course_code, Date)
        if session_id:
            attendance_data = analyzer.retrieve_attendance_data(session_id)
            data = analyzer.generate_final_conclusion(attendance_data)
            Final = analyzer.calculate_overall_status(data)
            analyzer.display_attendance(self.table, Final)  
        else:
            messagebox.showerror("Error", f"Session not found for course code: {course_code}")
    def on_close(self):
        self.destroy()
        self.main_app.deiconify()

