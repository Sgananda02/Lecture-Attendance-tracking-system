from MySQLdb import MySQLdb
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from datetime import date
from datetime import datetime
import datetime

class AttendanceAnalyzer:
    def __init__(self):
        self.db = MySQLdb('127.0.0.1', 'attendance_system', 'root', '')

    def get_schedule_id(self, course_code, day_of_week):
        connection = self.db.connect_to_database()
        cursor = connection.cursor()
        query = f"SELECT schedule_id FROM schedule WHERE Course_Code = '{course_code}' AND day_of_week = {day_of_week}"
        cursor.execute(query)
        schedule_id = cursor.fetchone()
        cursor.close()
        connection.close()
        return schedule_id[0] if schedule_id else None

    def get_session_id(self, course_code, Date):
        my_date = datetime.datetime.strptime(Date, "%d/%m/%Y")
        day_of_week = (int(my_date.strftime("%w")) - 1) % 7
        formatted_date = my_date.strftime("%Y-%m-%d")
        print(formatted_date)
        schedule_id = self.get_schedule_id(course_code, day_of_week)
        print(f"Schedule_id = {schedule_id}")
        if schedule_id:
            connection = self.db.connect_to_database()
            cursor = connection.cursor()
            query = f"SELECT session_id FROM class_sessions WHERE schedule_id = {schedule_id} AND session_date = '{formatted_date}'"
            cursor.execute(query)
            session_id = cursor.fetchone()
            cursor.close()
            connection.close()
            return session_id[0] if session_id else None
        else:
            return None


    def retrieve_attendance_data(self, session_id):
        connection = self.db.connect_to_database()
        cursor = connection.cursor()
        query = f"SELECT Student_number, attendance_status FROM attendance WHERE session_id = {session_id}"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    def generate_final_conclusion(self, data):
        final_conclusion = {}
        for row in data:
            student_number, attendance_status = row
            if student_number not in final_conclusion:
                final_conclusion[student_number] = []

            final_conclusion[student_number].append(attendance_status)
        print(final_conclusion)
        return final_conclusion

    def calculate_overall_status(self, final_conclusion):
        overall_status = {}
        for student_number, status_list in final_conclusion.items():
            present_count = status_list.count('Present')
            total_statuses = len(status_list)
            percentage_present = (present_count / total_statuses) * 100
            overall_status[student_number] = {
                'Status': 'Present' if percentage_present >= 50 else 'Absent',
                'Percentage': percentage_present
            }
        return overall_status


    def create_pdf(self, data, course_code):
        pdf_filename = f"{course_code}_attendance.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))
        elements = []

        # Title
        title = f"Attendance Data for {course_code}"
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="TitleStyle", parent=styles['Title'])
        title_style.fontName = 'Helvetica-Bold'  # Set the font to bold
        title_text = Paragraph(title, title_style)
        elements.append(title_text)
    

        table_data = [["Student Number", "Attendance Status", "Attendance Percentage"]]
        for student_number, info in data.items():
            attendance_status = info['Status']
            percentage_present = info['Percentage']
            table_data.append([student_number, attendance_status, f"{percentage_present:.2f}%"])

        table = Table(table_data, colWidths=[100, 100, 100], hAlign='CENTER')  # Adjust column widths as needed

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(PageBreak())  # Add a page break after the table

        doc.build(elements)
        print(f"PDF saved as {pdf_filename}")
        
    def display_attendance(self, table, data):
        for item in table.get_children():
            table.delete(item)
        
        for student_number, info in data.items():
            attendance_status = info['Status']
            percentage_present = info['Percentage']
            table.insert("", "end", values=(student_number, attendance_status, f"{percentage_present:.2f}%"))



 


