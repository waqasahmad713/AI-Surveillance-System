# import cv2
# import time
# import threading

# class CameraStream:
#     def __init__(self, cam_id, model, alert_system):
#         self.cam_id = cam_id
#         self.cap = cv2.VideoCapture(cam_id)
#         self.model = model
#         self.alert_system = alert_system
#         self.last_alert = 0
#         self.status = {"label": "OFF", "confidence": 0}

#     def read(self):
#         success, frame = self.cap.read()
#         if not success:
#             return None

#         results = self.model(frame)
#         annotated = results[0].plot()

#         detected = False
#         best_conf = 0

#         if results[0].boxes is not None:
#             for box in results[0].boxes:
#                 conf = float(box.conf[0])
#                 best_conf = max(best_conf, conf)
#                 if conf > 0.5:
#                     detected = True

#         self.status = {
#             "label": "ALERT" if detected else "SAFE",
#             "confidence": best_conf
#         }

#         # ALERT SYSTEM
#         now = time.time()
#         if detected and now - self.last_alert > 5:
#             self.alert_system.trigger(self.cam_id, frame)
#             self.last_alert = now

#         return annotated


# class CameraStreamManager:
#     def __init__(self, model_path):
#         from ultralytics import YOLO
#         self.model = YOLO(model_path)
#         self.cameras = {}
#         self.alert_system = None

#     def start(self, cam_id, alert_system):
#         self.alert_system = alert_system
#         if cam_id not in self.cameras:
#             self.cameras[cam_id] = CameraStream(cam_id, self.model, alert_system)

#     def stop(self, cam_id):
#         if cam_id in self.cameras:
#             self.cameras[cam_id].cap.release()
#             del self.cameras[cam_id]

#     def generate(self, cam_id):
#         cam = self.cameras.get(cam_id)

#         while True:
#             if cam is None:
#                 continue

#             frame = cam.read()
#             if frame is None:
#                 continue

#             _, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     def get_status(self, cam_id):
#         cam = self.cameras.get(cam_id)
#         if cam:
#             return cam.status
#         return {"label": "OFF", "confidence": 0}