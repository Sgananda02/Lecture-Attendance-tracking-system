import cv2
from retinaface import RetinaFace
import time
class RetinaFaceDetector:
    def __init__(self, min_confidence):
        self.min_confidence = min_confidence
    
    def detect(self, frame):
        start_time = time.time()
        faces_info = RetinaFace.detect_faces(frame)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        detected = []

        if isinstance(faces_info, dict):
            # Faces were detected
            for face_key, face_info in faces_info.items():
                if 'score' in face_info:
                    f_conf = face_info['score']
                    if f_conf >= self.min_confidence:
                        detected.append(face_info)
        else:
            # No faces were detected
            print("No faces detected in the frame.")
        return detected

    @staticmethod
    def extract(frame, face_info):
        (x1, y1, x2, y2) = face_info['facial_area']
        #(l_eye, r_eye, nose, mouth_l, mouth_r) = RetinaFaceDetector.get_keypoints(face_info)
        f_cropped = frame[y1:y2, x1:x2].copy()
        return ( f_cropped)

    @staticmethod
    def get_keypoints(face_info):
        keypoints = face_info['landmarks']
        l_eye = (int(keypoints['left_eye'][0]), int(keypoints['left_eye'][1]))
        r_eye = (int(keypoints['right_eye'][0]), int(keypoints['right_eye'][1]))
        nose = (int(keypoints['nose'][0]), int(keypoints['nose'][1]))
        mouth_l = (int(keypoints['mouth_left'][0]), int(keypoints['mouth_left'][1]))
        mouth_r = (int(keypoints['mouth_right'][0]), int(keypoints['mouth_right'][1]))
        return (l_eye, r_eye, nose, mouth_l, mouth_r)

    @staticmethod
    def draw_face(face_info, color, frame, draw_points=True, draw_rect=True, n_data=None):
        (x1, y1, x2, y2) = face_info['facial_area']
        confidence = face_info['score']

        if draw_rect:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)

        y3 = y1 - 12
        if not (n_data is None):
            (name, conf) = n_data
            text = name + (" %.3f" % conf)
        else:
            text = "%.3f" % confidence
        cv2.putText(frame, text, (x1, y3), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv2.LINE_AA)

        if draw_points:
            (l_eye, r_eye, nose, mouth_l, mouth_r) = RetinaFaceDetector.get_keypoints(face_info)
            RetinaFaceDetector.draw_point(l_eye, color, frame)
            RetinaFaceDetector.draw_point(r_eye, color, frame)
            RetinaFaceDetector.draw_point(nose, color, frame)
            RetinaFaceDetector.draw_point(mouth_l, color, frame)
            RetinaFaceDetector.draw_point(mouth_r, color, frame)

    @staticmethod
    def draw_point(point, color, frame):
        (x, y) = point
        x1 = x - 1
        y1 = y - 1
        x2 = x + 1
        y2 = y + 1
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)


