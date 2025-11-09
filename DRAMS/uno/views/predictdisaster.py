# import the necessary packages
from tensorflow.keras.models import load_model
from . import config
import numpy as np
import cv2


class PredictDisaster:
    def __init__(self):
        self.model = load_model(config.MODEL_PATH)
        self.W = None
        self.H = None
    
    def predict(self, frame):
        # load the trained model from disk
        print("[INFO] loading model and label binarizer...")
        model = load_model(config.MODEL_PATH)
        
        if self.W is None or self.H is None:
            (self.H, self.W) = frame.shape[:2]
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (224, 224))
        frame = frame.astype("float32")

        preds = model.predict(np.expand_dims(frame, axis=0))[0]

        return preds