import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from keras_facenet import FaceNet

# FaceNet recognizer
class FaceNetRec:    
    def __init__(self):
        self.face_recognizer = FaceNet()

    def embeddings(self, f_img):
        r_img = cv2.resize(f_img, (160, 160), cv2.INTER_AREA)
        samples = np.expand_dims(r_img, axis=0)
        embds = self.face_recognizer.embeddings(samples)  
        return embds[0]

    def resize_image(self, image, target_size=(160, 160)):
        image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        return image

    def normalize_image(self, image):
        # Normalize the pixel values to the [-1, 1] range
        image = (image / 255.0) * 2.0 - 1.0
        return image

    def encode_image(self, image):
        # Convert the preprocessed image to a NumPy array with appropriate dimensions
        image = image[np.newaxis, ...]
        return image
    
    def eval_distance(self, embds1, embds2):
        embds1 = np.squeeze(embds1)
        embds2 = np.squeeze(embds2)
        embds1 = embds1.reshape(1, -1)
        embds2 = embds2.reshape(1, -1)
        #cosine = np.sum(embds1*embds2, axis=1)/(norm(embds1, axis=1)*norm(embds2, axis=1))
        similarity  = cosine_similarity(embds1, embds2)
        return similarity [0][0]

    def img_distance(self, f_img1, f_img2):
        embds1 = self.embeddings(f_img1)
        embds2 = self.embeddings(f_img2)
        dist = self.eval_distance(embds1, embds2)
        return dist 
    
    def match(self, embds1, embds2):
        dist = self.eval_distance(embds1, embds2)
        return dist <= self.min_distance
    
    def img_match(self, f_img1, f_img2):
        embds1 = self.embeddings(f_img1)
        embds2 = self.embeddings(f_img2)
        return self.match(embds1, embds2)
    
    def recognize(self, embds, f_db):
        minfd = 2.0
        indx = -1
        f_data = f_db.get_data()
        for (i, data) in enumerate(f_data):
            (name, embds_i, p_img) = data
            dist = self.eval_distance(embds, embds_i)
            if (dist<minfd) and (dist<self.min_distance):
                indx = i
                minfd = dist
        if indx>=0:
            (name, embds_i, p_img) = f_data[indx]
            return (name, minfd, p_img)
        
        return None
    

