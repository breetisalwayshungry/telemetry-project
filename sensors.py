import serial
import time
import logger # CSV logger script
import transceiver # transceiver script
import threading # Allows tasks to run in parallel

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

sensor_data = {}

def read_sensor_data(): 
	global sensor_data
	try: 
		with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5) as ser:
			print("[INFO] Waiting for data...")
			while True: 
				line = ser.readline().decode("utf-8", errors="replace").strip()
				if line: 
					# print(f"[INFO] Received: {line}")
					sensor_data = parse_data(line)
					logger.log_data(sensor_data)
	except serial.SerialException as e: 
		print(f"[ERROR] Serial connection issue: {e}")
		logger.close_logger()
	except KeyboardInterrupt: 
		print("[INFO] Stopping sensor read.")
		logger.close_logger()

def parse_data(raw_line): 
	try: 
		return [float(x) for x in raw_line.split(", ")]
	except ValueError: 
		print(f"[WARNING] Invalid data format: {raw_line}")
		return []

def send_data(): 
	global sensor_data
	while True: 
		if sensor_data: 
			RF_line = ', '.join(map(str, sensor_data))
			print(f"[RF] Sending telem: {RF_line}")
			transceiver.send_telemetry(RF_line)
		time.sleep(1) # sends data at 1Hz

def main(): 
	# Initialize transceiver
	radio = transceiver.setup_radio()

	# Start threads for collection and transmission
	data_collection_thread = threading.Thread(target=read_sensor_data)
	data_collection_thread.start()

	data_sending_thread = threading.Thread(target=send_data)
	data_sending_thread.start()

	# Keep main thread alive to continue running
	data_collection_thread.join()
	data_sending_thread.join()

if __name__ == "__main__": 
	main()

