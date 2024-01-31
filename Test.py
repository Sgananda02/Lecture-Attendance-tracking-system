import os
import numpy as np
import copy
from Retinaface import RetinaFaceDetector
import cv2
import pickle
from keras_facenet import FaceNet
from MySQLdb import connect_to_database, insert_data, close_connection, check_student_exists
from FaceNet import FaceNetRec  # Import the FaceNetRec class from FaceNet.py

if __name__ == "__main__":
    # Initialize RetinaFaceDetector
    d = RetinaFaceDetector(min_confidence=0.5)

    # Create an instance of the FaceNetRec class
    min_distance_threshold = 0.5  # Adjust this threshold as needed
    face_recognizer = FaceNetRec(min_distance_threshold)

    parent_folder = "Student_Training"
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        exit()

    frame_number = 0
    # Prompt user for student information
    student_name = input("Enter student's name: ")
    student_surname = input("Enter student's surname: ")
    student_number = input("Enter student's number: ")
    student_folder_name = f"{student_name}_{student_surname}_{student_number}"
    student_folder_path = os.path.join(parent_folder, student_folder_name)
    if not os.path.exists(student_folder_path):
        os.makedirs(student_folder_path)
    # Establish a connection to the MySQL database
    db_connection = connect_to_database()
    data_to_insert1 = {
        "Student_Number": student_number,
        "First_Name": student_name,
        "Last_Name": student_number,
    }
    if not check_student_exists(db_connection, student_number):
        insert_data(db_connection, "student_table", data_to_insert1)
    else:
        print("Student already exists in the database.")

    print("\n[INFO] Initializing face capture. Look at the camera and wait ...")
    # Initialize variables
    count = 0  # Initialize face sample count

    # Capture faces and insert face recognition features
    while count < 10:  # Capture 10 face samples per person (modify as needed)
        ret, frame = cap.read()

        if not ret:
            break

        # Detect faces in the frame using RetinaFaceDetector
        faces_info = d.detect(frame)

        for i, face_info in enumerate(faces_info):
            count += 1
            f_cropped_info, f_img = d.extract(frame, face_info)

            x1, y1, x2, y2 = face_info['facial_area']
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Capture features from the detected face region
            #preprocessed_image = np.expand_dims(f_img, axis=0)  # Use the detected face region
            features = face_recognizer.embeddings(f_img)
            features_binary = pickle.dumps(features)
            data_to_insert = {
                "Student_Number": student_number,
                "Feature_Vector": features_binary,
            }
            table_name = "features"  # Make sure this matches your actual table name

            if insert_data(db_connection, table_name, data_to_insert):
                print("Data inserted successfully!")
            else:
                print("Failed to insert data.")

        # Display the frame with detected faces
        cv2.imshow('Camera Feed with Face Detection', frame)

        k = cv2.waitKey(1) & 0xff
        if k == 27:  # Press 'ESC' to exit
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    # Close the MySQL database connection
    close_connection(db_connection)
