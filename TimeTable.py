import cv2
import numpy as np
import pickle
import random
import time
from datetime import timedelta
from datetime import datetime as local_datetime
from MySQLdb import MySQLdb
from FaceNet import FaceNetRec  
from Retinaface import RetinaFaceDetector
import urllib.request

# Initialize 
face_recognizer = FaceNetRec()
face_detector = RetinaFaceDetector(min_confidence=0.7)

# Create a MySQLdb instance
db = MySQLdb('127.0.0.1', 'attendance_system', 'root', '')
connection = db.connect_to_database()
def format_timedelta(td):
    # Extract days, hours, minutes, and seconds from the timedelta object
    days = td.days
    seconds = td.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    # Create a formatted string
    formatted_time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    return formatted_time

def take_attendance_random_intervals():
    while True:
        schedule_id, module_name, class_start_time, end_time = db.retrieve_class_info()
        if module_name:
            # Check if a session with the same schedule_id and day already exists
            existing_session_id = db.check_existing_session(schedule_id, class_start_time, connection)

            if existing_session_id is None:
                # If no existing session found, insert a new session
                data_to_insert = {
                    "schedule_id": schedule_id,
                    "Start_time": class_start_time,
                    "End_time": end_time
                }
                table_name = "class_sessions"
                inserted = db.insert_data(connection,table_name, data_to_insert)

                if inserted:
                    session_id = db.get_last_insert_id(connection.cursor())
                else:
                    # Handle the case where insertion failed
                    print("Failed to insert new session.")
                    session_id = None
            else:
                # Use the existing session_id
                session_id = existing_session_id

            current_datetime = local_datetime.now()
            current_time = current_datetime.time()
            
            # Create a timedelta object with the extracted time
            current_time = timedelta(
                hours=current_time.hour,
                minutes=current_time.minute,
                seconds=current_time.second,
                microseconds=current_time.microsecond
            )

            if current_time <= class_start_time :
                class_duration = (end_time - class_start_time).total_seconds()
                Interval_increase = class_duration / 4
            else:
                class_duration = (end_time - current_time).total_seconds()
                Interval_increase = class_duration / 4 
                
            print("Class has Started!!")
            while True:
                #ret, frame = camera.read()
                print("Taking the Image...")
                imgResponse = urllib.request.urlopen('http://192.168.8.116/capture')
                imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
                frame = cv2.imdecode(imgNp,-1)
                print("Image Taken")
                #if not ret:
                 #   break

                if class_start_time <= current_time <= end_time:
                    labels, feature_vectors,enrolled_students = db.load_face_recognition_data(connection,module_name)
                    detected_faces = face_detector.detect(frame)  # Use RetinaFace for face detection

                    recognized_students = []  # List to store recognized people's names and information
                    for face_info in detected_faces:
                        x1, y1, x2, y2 = face_info['facial_area']
                        face_img = frame[y1:y2, x1:x2]  # Extract the detected face from the frame
                        query_feature = face_recognizer.embeddings(face_img)

                        # Compare the query feature with features in the database using cosine distance
                        found = False
                        for label, feature_vector in zip(labels, feature_vectors):
                            cosine_distance = face_recognizer.eval_distance(query_feature, feature_vector)

                            if cosine_distance > 0.75:
                                print("Person recognized as Student_Number:", label)
                                recognized_students.append({
                                    "Student_Number": label,
                                })
                                found = True
                                break
                        if not found:
                            print("Person not recognized.")

                        # Draw a rectangle around the recognized face
                        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    save_attendance(recognized_students, enrolled_students, session_id)
                    current_time = current_time.total_seconds()
                    current_time += Interval_increase
                    current_time = timedelta(seconds=current_time)
                    formatted_interval = format_timedelta(timedelta(seconds=Interval_increase))
                    print(f"Next attendance at {current_time} ({formatted_interval})")
                    
                    if current_time >= end_time:
                        break
                    else:
                        Sleep_time = Interval_increase - 35
                        time.sleep(Sleep_time)

                if cv2.waitKey(1) & 0xFF == ord('q') or current_time >= end_time:
                    break

            cv2.destroyAllWindows()
            break
        else:
            random_interval = random.randint(20, 30)
            print(f"Module not found. Waiting for {random_interval} seconds before checking again...")
            time.sleep(random_interval)

def save_attendance(recognized_students, all_students, session_id):
    recognized_student_numbers = [student['Student_Number'] for student in recognized_students]

    for student_number in all_students:
        if student_number in recognized_student_numbers:
            # Student is recognized, mark attendance as "Present"
            attendance_status = "Present"
        else:
            # Student is not recognized, mark attendance as "Absent"
            attendance_status = "Absent"
        
        data_to_insert = {
            "Student_Number": student_number,
            "session_id": session_id,
            "attendance_status": attendance_status
        }
        table_name = "attendance"
        db.insert_data(connection, table_name, data_to_insert)
    
    recognized_students.clear()

    
take_attendance_random_intervals()
