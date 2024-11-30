import serial
import csv
from datetime import datetime
import pytz

timezone = pytz.timezone('US/Eastern')
serial_port = '/dev/ttyUSB1'  #
baud_rate = 115200 

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Connected to {serial_port}")
except Exception as e:
    print(f"Failed to connect to {serial_port}: {e}")
    exit(1)

filename = "temperature_log.csv"

try:
    with open(filename, mode='r') as file:
        is_empty = file.read(1) == '' 
except FileNotFoundError:
    is_empty = True  

with open(filename, mode='a', newline='') as file:
    csv_writer = csv.writer(file)

    if is_empty:  
        csv_writer.writerow(["Timestamp", "Temperature (°C)", "Temperature (°F)"])

    print(f"Logging data to {filename}...")

    try:
        temp_c = None
        temp_f = None

        while True:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            if "Temperature (°C)" in line:
                temp_c = line.split(": ")[1].replace("°C", "").strip()
            if "Temperature (°F)" in line:
                temp_f = line.split(": ")[1].replace("°F", "").strip()
            if temp_c is not None and temp_f is not None:
                timestamp = datetime.now(timezone).strftime("%m-%d-%Y %I:%M%p")
                csv_writer.writerow([timestamp, temp_c, temp_f])
                file.flush()
                print(f"{timestamp} - Temp (°C): {temp_c}, Temp (°F): {temp_f}")
                temp_c = None
                temp_f = None
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()
        print("Serial connection closed.")
