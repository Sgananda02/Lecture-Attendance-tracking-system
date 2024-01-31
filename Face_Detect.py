import cv2
import numpy as np
from Retinaface import RetinaFaceDetector
import urllib.request

class FaceDetection:
    def __init__(self):
        self.face_detector = RetinaFaceDetector(min_confidence=0.7)
        
    def update_camera_frame(self, frame):
        Image1 = 'Detected Face'
        cv2.namedWindow(Image1, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(Image1, width=698, height=491)
        cv2.imshow(Image1, frame)
        cv2.moveWindow(Image1, 348, 60)
        cv2.waitKey(0)
        
    def detect_faces_show_confidence(self):
        
        imgResponse = urllib.request.urlopen('http://192.168.8.116/capture')
        imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)
        print("Image Taken")
        detected_faces = self.face_detector.detect(frame)

        for face_info in detected_faces:
            x1, y1, x2, y2 = face_info['facial_area']
            confidence = face_info['score']
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Display confidence score on the image
            cv2.putText(frame, f"Confidence: {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        self.update_camera_frame(frame)
        cv2.destroyAllWindows()


