import serial
import csv
import cv2
from datetime import datetime
import pytz
import time

esp32_serial_port = '/dev/ttyUSB1'  
camera_index = 0  
baud_rate = 115200  
timezone = pytz.timezone('US/Eastern')
filename = "temperature_log.csv"


try:
    esp32_serial = serial.Serial(esp32_serial_port, baud_rate, timeout=1)
    print(f"Connected to ESP32 on {esp32_serial_port}")
except Exception as e:
    print(f"Failed to connect to ESP32 on {esp32_serial_port}: {e}")
    exit(1)

try:
    with open(filename, mode='r') as file:
        is_empty = file.read(1) == '' 
except FileNotFoundError:
    is_empty = True 

with open(filename, mode='a', newline='') as file:
    csv_writer = csv.writer(file)

    if is_empty:  
        csv_writer.writerow(["Timestamp", "Temperature (°C)", "Temperature (°F)", "Image Filename"])

    print(f"Logging data to {filename}...")

    try:
        while True:
            temp_c = None
            temp_f = None
            while True:
                line = esp32_serial.readline().decode('utf-8').strip()
                print(f"ESP32: {line}")  

                if "Temperature (°C)" in line:
                    temp_c = line.split(": ")[1].replace("°C", "").strip()

                if "Temperature (°F)" in line:
                    temp_f = line.split(": ")[1].replace("°F", "").strip()

                if temp_c is not None and temp_f is not None:
                    break

            now = datetime.now(timezone)
            timestamp = now.strftime("%m-%d-%Y %I:%M%p")
            image_filename = now.strftime("Pictures/%m-%d-%Y-%I:%M%p.jpg")

            cap = cv2.VideoCapture(camera_index)  
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(image_filename, frame)
                print(f"Image saved as {image_filename}")
            else:
                print("Failed to capture image.")
            cap.release()

            csv_writer.writerow([timestamp, temp_c, temp_f, image_filename])
            file.flush()  
            print(f"{timestamp} - Temp (°C): {temp_c}, Temp (°F): {temp_f}, Image: {image_filename}")

            time.sleep(300)

    except KeyboardInterrupt:
        print("\nProcess stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        esp32_serial.close()
        print("ESP32 serial connection closed.")
