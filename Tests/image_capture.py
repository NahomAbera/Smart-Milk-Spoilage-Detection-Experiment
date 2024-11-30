import cv2
import time
from datetime import datetime
import pytz

def capture_image(camera_index=0):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Unable to access the camera.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Unable to capture an image.")
                break

            timezone = pytz.timezone('US/Eastern') 
            now = datetime.now(timezone)
            filename = now.strftime("%m-%d-%Y-%I:%M%p.jpg")

            cv2.imwrite(filename, frame)
            print(f"Image saved as {filename}")

            time.sleep(300)  # wait for 300 seconds (5 min)
    except KeyboardInterrupt:
        print("\nStopping the image capture process.")
    finally:
        cap.release()
        print("Camera released.")

if __name__ == "__main__":
    capture_image()

