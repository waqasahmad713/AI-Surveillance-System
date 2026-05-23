# import threading
# import cv2
# import time
# from twilio.rest import Client

# class AlertSystem:

#     def __init__(self):
#         self.cooldown = {}

#         self.client = Client(
#             "YOUR_TWILIO_SID",
#             "YOUR_TWILIO_AUTH"
#         )

#     def trigger(self, cam_id, frame):

#         now = time.time()

#         if cam_id in self.cooldown:
#             if now - self.cooldown[cam_id] < 5:
#                 return

#         self.cooldown[cam_id] = now

#         # Save image
#         path = f"static/alerts/cam_{cam_id}_{int(now)}.jpg"
#         cv2.imwrite(path, frame)

#         # Send WhatsApp (image)
#         threading.Thread(target=self.send_whatsapp, args=(path,), daemon=True).start()

#     def send_whatsapp(self, image_path):

#         try:
#             message = self.client.messages.create(
#                 from_="whatsapp:+14155238886",
#                 to="whatsapp:+92YOURNUMBER",
#                 media_url=[f"http://your-server/{image_path}"],
#                 body="🚨 AI ALERT: Threat detected!"
#             )

#             print("WhatsApp alert sent")

#         except Exception as e:
#             print("WhatsApp error:", e)