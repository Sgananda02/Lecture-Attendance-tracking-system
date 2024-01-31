import os
import numpy as np
from Retinaface import RetinaFaceDetector
import cv2
import pickle
from MySQLdb import MySQLdb
from FaceNet import FaceNetRec
import time
import urllib.request

class StudentRegister:
    def __init__(self):
        self.d = RetinaFaceDetector(min_confidence=0.7)
        self.face_recognizer = FaceNetRec()
        self.parent_folder = "Student_Training"
        self.db = MySQLdb('127.0.0.1', 'attendance_system', 'root', '')  
        self.connection = self.db.connect_to_database()
        self.student_number = None
        self.student_name = None
        self.student_surname = None
        self.student_folder_path = None
        self.photo = None

    def update_camera_frame(self, frame):
        Image1 = 'Detected Face'
        cv2.namedWindow(Image1, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(Image1, width=698, height=491)
        cv2.imshow(Image1, frame)
        cv2.moveWindow(Image1, 348, 60)
        cv2.waitKey(1)

    def capture_faces(self, student_name, student_surname, student_number):
        self.student_name = student_name
        self.student_surname = student_surname
        self.student_number = student_number

        self.student_folder_name = f"{self.student_name}_{self.student_surname}_{self.student_number}"
        self.student_folder_path = os.path.join(self.parent_folder, self.student_folder_name)
        if not os.path.exists(self.student_folder_path):
            os.makedirs(self.student_folder_path)

        data_to_insert1 = {
            "Student_Number": self.student_number,
            "First_Name": self.student_name,
            "Last_Name": self.student_surname,
        }
        if not self.db.check_student_exists(self.connection, self.student_number):
            self.db.insert_data(self.connection, "student_table", data_to_insert1)
        else:
            print("Student already exists in the database.")

        print("\n[INFO] Initializing face capture. Look at the camera and wait ...")

        captured_images = []
        count = 0  # Initialize face sample count

        while count < 1:  # Capture 3 face samples per person
            imgResponse = urllib.request.urlopen('http://192.168.8.116/capture')
            imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgNp, -1)
            captured_images.append(frame)
            count += 1
            print(f"Image{count}")
            k = cv2.waitKey(1) & 0xff
            if k == 27 or count == 1:  # Press 'ESC' or captured 3 samples to exit
                break

        cv2.destroyAllWindows()
        print("\nImages Taken sucessfully")
        # Process the captured images for face detection and feature extraction
        face_images = []
        start_time = time.time()
        for img in captured_images:
            faces_info = self.d.detect(img)
            face_info = faces_info[0]
            x1, y1, x2, y2 = face_info['facial_area']
            f_img = img[y1:y2, x1:x2]
            face_images.append(f_img)  
            
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        # Compute embeddings for all stored face images
        embeddings_list = [self.face_recognizer.embeddings(face_img) for face_img in face_images]

        # Insert the computed embeddings into the database
        table_name = "features"
        for features in embeddings_list:
            features_binary = pickle.dumps(features)
            data_to_insert = {
                "Student_Number": self.student_number,
                "Feature_Vector": features_binary,
            }
            if self.db.insert_data(self.connection, table_name, data_to_insert):
                print("Data inserted successfully!")
            else:
                print("Failed to insert data.")

    def close_db_connection(self):
        # Close the MySQL database connection
        self.db.close_connection()
