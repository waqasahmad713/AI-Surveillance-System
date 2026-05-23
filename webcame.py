# from flask import Flask, render_template, Response, jsonify
# from ultralytics import YOLO
# import cv2
# import time
# import threading
# from playsound import playsound

# app = Flask(__name__)

# # Load YOLO model
# model = YOLO("/home/waqas-ahmad/Desktop/models/model/best.pt")

# # Camera (AUTO FIXED fallback)
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     cap = cv2.VideoCapture(1)
# if not cap.isOpened():
#     cap = cv2.VideoCapture(2)

# # System state
# system_running = False
# last_alert_time = 0
# ALERT_COOLDOWN = 5

# status = {
#     "label": "SYSTEM OFF",
#     "confidence": 0.0
# }

# # Alert function
# def play_alert():
#     try:
#         playsound("alart.mp3")
#     except:
#         print("⚠️ Alarm sound error")

# # Frame generator
# def generate_frames():
#     global system_running, last_alert_time, status

#     while True:

#         if not system_running:
#             time.sleep(0.1)
#             continue

#         success, frame = cap.read()
#         if not success:
#             continue

#         results = model(frame)
#         annotated = results[0].plot()

#         boxes = results[0].boxes
#         detected = False
#         best_conf = 0

#         if boxes is not None:
#             for box in boxes:
#                 conf = float(box.conf[0])
#                 best_conf = max(best_conf, conf)

#                 if conf > 0.5:
#                     detected = True

#         # Update status
#         status["confidence"] = best_conf
#         status["label"] = "🚨 DETECTED" if detected else "SAFE"

#         # ALERT SYSTEM
#         current_time = time.time()

#         if detected and (current_time - last_alert_time > ALERT_COOLDOWN):
#             print("🚨 ALERT TRIGGERED")

#             threading.Thread(target=play_alert, daemon=True).start()

#             last_alert_time = current_time

#         # Encode frame
#         ret, buffer = cv2.imencode('.jpg', annotated)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# # Routes
# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/video')
# def video():
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/start')
# def start():
#     global system_running
#     system_running = True
#     return jsonify({"status": "started"})


# @app.route('/stop')
# def stop():
#     global system_running
#     system_running = False
#     return jsonify({"status": "stopped"})


# @app.route('/status')
# def get_status():
#     return jsonify(status)


# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, render_template, Response, jsonify
# from ultralytics import YOLO
# import cv2
# import time
# import threading
# from playsound import playsound

# app = Flask(__name__)

# # =====================
# # MODEL
# # =====================
# model = YOLO("/home/waqas-ahmad/Desktop/models/model/best.pt")

# ALERT_COOLDOWN = 5

# # =====================
# # GLOBAL STORAGE
# # =====================
# cameras = {}
# camera_status = {}

# # =====================
# # ALERT SOUND
# # =====================
# def play_alert():
#     try:
#         playsound("alart.mp3")
#     except Exception as e:
#         print("Sound error:", e)

# # =====================
# # CAMERA CLASS
# # =====================
# class CameraStream:
#     def __init__(self, cam_id):
#         self.cam_id = cam_id
#         self.cap = cv2.VideoCapture(cam_id)
#         self.last_alert = 0

#     def get_frame(self):
#         success, frame = self.cap.read()

#         if not success:
#             return None

#         results = model(frame)
#         annotated = results[0].plot()

#         detected = False
#         best_conf = 0.0

#         if results[0].boxes is not None:
#             for box in results[0].boxes:
#                 conf = float(box.conf[0])
#                 best_conf = max(best_conf, conf)
#                 if conf > 0.5:
#                     detected = True

#         # update status
#         camera_status[self.cam_id] = {
#             "status": "🚨 ALERT" if detected else "SAFE",
#             "confidence": best_conf
#         }

#         # ALERT SYSTEM
#         now = time.time()

#         if detected and (now - self.last_alert > ALERT_COOLDOWN):
#             print(f"🚨 ALERT CAMERA {self.cam_id}")

#             threading.Thread(target=play_alert, daemon=True).start()

#             self.last_alert = now

#         return annotated

#     def release(self):
#         self.cap.release()

# # =====================
# # STREAM GENERATOR
# # =====================
# def generate(camera_id):
#     cam_id = int(camera_id)

#     if cam_id not in cameras:
#         cameras[cam_id] = CameraStream(cam_id)

#     cam = cameras[cam_id]

#     while True:
#         frame = cam.get_frame()

#         if frame is None:
#             continue

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# # =====================
# # ROUTES
# # =====================
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video/<camera_id>')
# def video(camera_id):
#     return Response(generate(camera_id),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/status/<camera_id>')
# def status(camera_id):
#     cam_id = int(camera_id)
#     return jsonify(camera_status.get(cam_id, {"status": "OFF", "confidence": 0}))

# @app.route('/start/<camera_id>')
# def start(camera_id):
#     cam_id = int(camera_id)

#     if cam_id not in cameras:
#         cameras[cam_id] = CameraStream(cam_id)

#     return jsonify({"status": "started", "camera": cam_id})

# @app.route('/stop/<camera_id>')
# def stop(camera_id):
#     cam_id = int(camera_id)

#     if cam_id in cameras:
#         cameras[cam_id].release()
#         del cameras[cam_id]

#     return jsonify({"status": "stopped", "camera": cam_id})

# # =====================
# # RUN
# # =====================
# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)


from flask import Flask, render_template, Response, jsonify, request, redirect, session
from ultralytics import YOLO
import cv2
import time
import threading
from functools import wraps
from playsound import playsound

app = Flask(__name__)
app.secret_key = "super_secret_key_change_it"

# =====================
# MODEL
# =====================
model = YOLO("/home/waqas-ahmad/Desktop/models/model/best.pt")

ALERT_COOLDOWN = 5
cameras = {}
camera_status = {}

# =====================
# LOGIN CREDENTIALS (CHANGE THIS)
# =====================
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# =====================
# LOGIN REQUIRED DECORATOR
# =====================
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrap

# =====================
# ALERT SOUND
# =====================
def play_alert():
    try:
        playsound("alart.mp3")
    except:
        print("Sound error")

# =====================
# CAMERA CLASS
# =====================
class CameraStream:
    def __init__(self, cam_id):
        self.cam_id = cam_id
        self.cap = cv2.VideoCapture(cam_id)
        self.last_alert = 0

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        results = model(frame)
        annotated = results[0].plot()

        detected = False
        best_conf = 0

        if results[0].boxes is not None:
            for box in results[0].boxes:
                conf = float(box.conf[0])
                best_conf = max(best_conf, conf)
                if conf > 0.5:
                    detected = True

        camera_status[self.cam_id] = {
            "status": "🚨 ALERT" if detected else "SAFE",
            "confidence": best_conf
        }

        now = time.time()
        if detected and (now - self.last_alert > ALERT_COOLDOWN):
            threading.Thread(target=play_alert, daemon=True).start()
            self.last_alert = now

        return annotated

# =====================
# STREAM
# =====================
def generate(camera_id):
    cam_id = int(camera_id)

    if cam_id not in cameras:
        cameras[cam_id] = CameraStream(cam_id)

    cam = cameras[cam_id]

    while True:
        frame = cam.get_frame()
        if frame is None:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# =====================
# LOGIN PAGE
# =====================
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["logged_in"] = True
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# =====================
# LOGOUT
# =====================
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

# =====================
# DASHBOARD (PROTECTED)
# =====================
@app.route('/')
@login_required
def index():
    return render_template("index.html")

# =====================
# VIDEO STREAM
# =====================
@app.route('/video/<camera_id>')
@login_required
def video(camera_id):
    return Response(generate(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# =====================
# STATUS
# =====================
@app.route('/status/<camera_id>')
@login_required
def status(camera_id):
    return jsonify(camera_status.get(int(camera_id), {"status": "OFF"}))

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(debug=True, threaded=True)