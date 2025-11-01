# USAGE:
# python predict.py --input (fire/flood video).mp4 --output output/natural_disasters.avi

# 🔥 Prediction for Fire and Flood Added (auto-selects model based on video name)

from tensorflow.keras.models import load_model
from flooddetector import config
from collections import deque
import numpy as np
import argparse
import cv2
import os

# ---------------- Argument Setup ----------------
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

# ---------------- Model Selection ----------------
video_name = args["input"].lower()

if "fire" in video_name:
	print("[INFO] 🔥 Fire video detected. Loading Fire model...")
	model = load_model("output/Fire.model")
	disaster_type = "Fire"
elif "flood" in video_name:
	print("[INFO] 🌊 Flood video detected. Loading Flood model...")
	model = load_model("output/Flood.model")
	disaster_type = "Flood"
else:
	print("[WARN] ⚠️ Unknown video type. Defaulting to Flood model...")
	model = load_model("output/Flood.model")
	disaster_type = "Flood"

Q = deque(maxlen=args["size"])

print(f"[INFO] Processing video for {disaster_type} detection...")
vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)

# ---------------- Frame Loop ----------------
while True:
	(grabbed, frame) = vs.read()
	if not grabbed:
		break

	if W is None or H is None:
		(H, W) = frame.shape[:2]

	output = frame.copy()
	frame_resized = cv2.resize(frame, (224, 224))
	frame_resized = frame_resized.astype("float32") / 255.0

	# Prediction
	preds = model.predict(np.expand_dims(frame_resized, axis=0))[0]
	Q.append(preds)
	results = np.array(Q).mean(axis=0)
	i = np.argmax(results)
	confidence = results[i]

	# Label assignment
	if confidence < 0.5:
		label = "No Disaster Detected"
	else:
		label = f"{disaster_type} ({confidence:.2f})"

	# Display text
	color = (0, 0, 255) if disaster_type == "Fire" else (255, 0, 0)
	cv2.putText(output, f"Activity: {label}", (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
		1.25, color, 5)

	# Video writing setup
	if writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30, (W, H), True)

	writer.write(output)

	if args["display"] > 0:
		cv2.imshow("Output", output)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

# ---------------- Cleanup ----------------
print("[INFO] Cleaning up...")
writer.release()
vs.release()
cv2.destroyAllWindows()
