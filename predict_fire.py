# USAGE
# python predict.py --input (fire/flood video).mp4 --output output/natural_disasters.avi

# Prediction for fire and flood added 

from tensorflow.keras.models import load_model
from firedetector import config
from collections import deque
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to our input video")
ap.add_argument("-o", "--output", required=True,
	help="path to our output video")
ap.add_argument("-s", "--size", type=int, default=128,
	help="size of queue for averaging")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed to screen")
args = vars(ap.parse_args())

print("[INFO] loading model and label binarizer...")
model = load_model(config.MODEL_PATH)

Q = deque(maxlen=args["size"])

print("[INFO] processing video...")
vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)
 
while True:
	(grabbed, frame) = vs.read()
 
	if not grabbed:
		break
 
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	output = frame.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = cv2.resize(frame, (224, 224))
	frame = frame.astype("float32")
	
	preds = model.predict(np.expand_dims(frame, axis=0))[0]
	Q.append(preds)

	results = np.array(Q).mean(axis=0)
	i = np.argmax(results)
	if i==0:
		label = "Nothing"
	else:
		label = config.CLASSES[i]

	text = "activity: {}".format(label)
	cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
		1.25, (0, 255, 0), 5)
 
	if writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(W, H), True)
 
	writer.write(output)
 
	if args["display"] > 0:
		cv2.imshow("Output", output)
		key = cv2.waitKey(1) & 0xFF
	 
		if key == ord("q"):
			break
 
print("[INFO] cleaning up...")
writer.release()
vs.release()
