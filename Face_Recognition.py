import cv2
import numpy as np
from MySQLdb import MySQLdb
from FaceNet import FaceNetRec  
from Retinaface import RetinaFaceDetector
import urllib.request
import time

class FaceRecognition:
    def __init__(self):
        self.face_recognizer = FaceNetRec()
        self.face_detector = RetinaFaceDetector(min_confidence=0.7)
        # Create a MySQLdb instance
        self.db = MySQLdb('127.0.0.1', 'attendance_system', 'root', '')
        self.connection = self.db.connect_to_database()
        
    def update_camera_frame(self, frame):
        Image1 = 'Detected Face'
        cv2.namedWindow(Image1, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(Image1, width=698, height=491)
        cv2.imshow(Image1, frame)
        cv2.moveWindow(Image1, 348, 60)
        cv2.waitKey(0)  # Display the image until any key is pressed
        
    def recognize_people_from_image(self):
        labels, feature_vectors = self.db.retrieve_feature_vectors_and_labels(self.connection)  # Load face recognition data

        imgResponse = urllib.request.urlopen('http://192.168.8.116/capture')
        imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)
        print("Image Taken")
        
        start_time = time.time()
        detected_faces = self.face_detector.detect(frame)  # Use RetinaFace for face detection
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        
        for face_info in detected_faces:
            x1, y1, x2, y2 = face_info['facial_area']
            face_img = frame[y1:y2, x1:x2]  # Extract the detected face from the frame
            query_feature = self.face_recognizer.embeddings(face_img)

            found = False
            for label, feature_vector in zip(labels, feature_vectors):
                cosine_distance = self.face_recognizer.eval_distance(query_feature, feature_vector)
                print(f"flabel={label} has {cosine_distance}")
                    
                if cosine_distance > 0.75:
                    print("Person recognized as Student_Number:", label)
                    found = True
                    break

            if not found:
                label = "Unknown"
                print("Person not recognized.")

            # Draw a rectangle around the recognized face and display student number
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, str(label), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            
        
        self.update_camera_frame(frame)
        cv2.destroyAllWindows()


