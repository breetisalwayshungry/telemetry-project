import csv
import time
import os

BUFFER_SIZE = 50 # number of entries before writing to disk
data_buffer = [] # initialize buffer

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"log_{time.strftime('%Y%m%d_%H%M%S')}.csv")

def initialize_log():
	with open(log_file, mode="w", newline="") as f: 
		csv_writer = csv.writer(f)
		csv_writer.writerow(["Timestamp (Pi)", "Timestamp (Ard)", "Temperature", "Pressure", "Altitude", "AccelX", "AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ", "Lat", "Lon", "GPS Alt", "GPS Speed", "Sat Count"])

def log_data(sensor_data): 
	global data_buffer
	if not sensor_data: 
		return

	timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	data_buffer.append([timestamp] + sensor_data)

	if len(data_buffer) >= BUFFER_SIZE: 
		flush_buffer()

def flush_buffer():
	global data_buffer
	if data_buffer:
		with open(log_file, mode="a", newline="") as f: 
			csv_writer = csv.writer(f)
			csv_writer.writerows(data_buffer)
		print(f"<logger.py> [INFO] Flushed {len(data_buffer)} entries to CSV.")
		data_buffer = []

def close_logger():
	flush_buffer()

initialize_log()
