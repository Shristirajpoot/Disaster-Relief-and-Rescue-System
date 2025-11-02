from flooddetector.prediction_on_video import PredictDisaster
from flask import Flask, render_template, Response, jsonify
from collections import deque
from gradcam_visualizer import generate_gradcam_image
from dotenv import load_dotenv
from twilio.rest import Client
import numpy as np
import threading
import argparse
import cv2
import os
import time
from datetime import datetime
import winsound
import subprocess

# ------------------- Load Environment Variables -------------------
load_dotenv()
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
EMERGENCY_CONTACT_NUMBER = os.getenv("EMERGENCY_CONTACT_NUMBER")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# ------------------- Argument Parsing -------------------
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to input video")
ap.add_argument("-ip", "--ip", type=str, required=True, help="IP address of the device")
ap.add_argument("-o", "--port", type=int, required=True, help="Port number (1024–65535)")
ap.add_argument("-s", "--size", type=int, default=128, help="Queue size for averaging")
args = vars(ap.parse_args())

# ------------------- Flask Setup -------------------
app = Flask(__name__)
outputFrame = None
lock = threading.Lock()
Q = deque(maxlen=args["size"])
vs = cv2.VideoCapture(args["input"])

# ------------------- Alert Setup -------------------
os.makedirs("alert_snapshots", exist_ok=True)
os.makedirs("static/output", exist_ok=True)  # store Grad-CAM & prediction outputs
fire_count, flood_count = 0, 0
current_status = "Analyzing..."
alert_active = False
last_sms_time = 0  # SMS cooldown

# ------------------- Alert Functions -------------------
def play_alert_sound():
    try:
        winsound.Beep(1200, 400)
    except Exception as e:
        print(f"[WARN] Sound alert failed: {e}")

def save_alert_frame(frame, label):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"alert_snapshots/{label}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[ALERT] Snapshot saved: {filename}")

def send_sms_alert(label, confidence):
    """Send SMS using Twilio with cooldown to prevent spam"""
    global last_sms_time
    now = time.time()
    if now - last_sms_time < 60:  # 60 seconds cooldown
        print("[INFO] SMS alert skipped (cooldown active).")
        return

    last_sms_time = now
    try:
        message = client.messages.create(
            body=f"🚨 ALERT: {label} detected! Confidence: {confidence:.2f}. Please take immediate action!",
            from_=TWILIO_PHONE_NUMBER,
            to=EMERGENCY_CONTACT_NUMBER
        )
        print(f"[SMS SENT] {label} alert sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"[ERROR] Failed to send SMS alert: {e}")

# ------------------- Video Prediction -------------------
def predict_frame():
    global vs, outputFrame, lock, fire_count, flood_count, current_status, alert_active
    pd = PredictDisaster()

    while True:
        (grabbed, frame) = vs.read()
        if not grabbed:
            break

        frame_preds = pd.predict(frame)
        if frame_preds is not None:
            Q.append(frame_preds)
            results = np.array(Q).mean(axis=0)
            i = np.argmax(results)
            confidence = results[i]

            # Fire Detection
            if i == 1:
                label, color = "🔥 FIRE", (0, 0, 255)
                fire_count += 1
                current_status = f"🔥 Fire Detected ({confidence:.2f})"
                alert_active = True
                play_alert_sound()
                save_alert_frame(frame, "FIRE")
                send_sms_alert("FIRE", confidence)

                # ✅ Save unique Grad-CAM per detection
                timestamp = int(time.time())
                gradcam_path = f"static/output/gradcam_fire_{timestamp}.jpg"
                generate_gradcam_image("output/Fire.model", frame, gradcam_path)

            # Flood Detection
            elif i == 0:
                label, color = "🌊 FLOOD", (255, 0, 0)
                flood_count += 1
                current_status = f"🌊 Flood Detected ({confidence:.2f})"
                alert_active = True
                play_alert_sound()
                save_alert_frame(frame, "FLOOD")
                send_sms_alert("FLOOD", confidence)

                # ✅ Save unique Grad-CAM per detection
                timestamp = int(time.time())
                gradcam_path = f"static/output/gradcam_flood_{timestamp}.jpg"
                generate_gradcam_image("output/Flood.model", frame, gradcam_path)

            # Safe
            else:
                label, color = "✅ SAFE", (0, 255, 0)
                current_status = "✅ Safe"
                alert_active = False

            # Overlay info
            text = f"{label} | Confidence: {confidence:.2f}"
            cv2.putText(frame, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
            timestamp_str = datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, f"Time: {timestamp_str}", (35, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"🔥 Fires: {fire_count} | 🌊 Floods: {flood_count}",
                        (35, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 255, 0), 2)

        with lock:
            outputFrame = frame.copy()

# ------------------- Frame Stream -------------------
def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" +
               bytearray(encodedImage) +
               b"\r\n")

# ------------------- Routes -------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/alert")
def alert():
    if "Fire" in current_status:
        return jsonify({"alert": "🔥 EMERGENCY! Fire detected nearby. Evacuate immediately!"})
    elif "Flood" in current_status:
        return jsonify({"alert": "🌊 EMERGENCY! Flood detected in your area. Move to higher ground!"})
    else:
        return jsonify({"alert": ""})

@app.route("/status")
def status():
    return jsonify({
        "status": current_status,
        "fire_count": fire_count,
        "flood_count": flood_count
    })

@app.route("/gradcam_feed")
def gradcam_feed():
    """Serve latest Grad-CAM image."""
    files = sorted(
        [f for f in os.listdir("static/output") if f.startswith("gradcam_")],
        key=lambda x: os.path.getmtime(os.path.join("static/output", x)),
        reverse=True
    )
    if files:
        latest_file = os.path.join("static/output", files[0])
        return Response(open(latest_file, "rb").read(), mimetype="image/jpeg")
    else:
        return jsonify({"message": "Grad-CAM not available yet."}), 404

# ------------------- NEW: Offline Prediction Routes -------------------
@app.route("/predict_fire")
def predict_fire():
    """Run offline Fire prediction and display result."""
    cmd = "python predict_fire.py --input videos/video-1596442227.mp4 --output static/output/fire_detected.avi"
    subprocess.run(cmd, shell=True)
    return render_template("predict_result.html", video="static/output/fire_detected.avi")

@app.route("/predict_flood")
def predict_flood():
    """Run offline Flood prediction and display result."""
    cmd = "python predict_flood.py --input videos/Assam_floods.mp4 --output static/output/flood_detected.avi"
    subprocess.run(cmd, shell=True)
    return render_template("predict_result.html", video="static/output/flood_detected.avi")

# ------------------- Disable Caching -------------------
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ------------------- Main -------------------
if __name__ == "__main__":
    print("[INFO] Starting AI Disaster Relief System...")
    t = threading.Thread(target=predict_frame)
    t.daemon = True
    t.start()
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
