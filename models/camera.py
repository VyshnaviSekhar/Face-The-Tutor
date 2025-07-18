import cv2
import time
from backend.notification import send_notification_to_student

def is_student_unfocused(frame):
    return False  # Placeholder logic

def gen_frames(student_username=None):
    cap = cv2.VideoCapture(0)
    last_alert_time = 0
    unfocused_start = None
    alert_interval = 10 * 60  # 10 minutes

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (640, 480))

        if is_student_unfocused(frame):
            if unfocused_start is None:
                unfocused_start = time.time()
            elif time.time() - unfocused_start >= alert_interval and time.time() - last_alert_time >= alert_interval:
                send_notification_to_student(student_username, "You have been unfocused for over 10 minutes.")
                last_alert_time = time.time()
        else:
            unfocused_start = None

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
