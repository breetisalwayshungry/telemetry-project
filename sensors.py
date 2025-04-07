import serial
import time
import logger # CSV logger script
import transceiver # transceiver script
import threading # Allows tasks to run in parallel

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

sensor_data = []
gps_buffer = [None] * 5

def read_sensor_data(): 
	global sensor_data
	try: 
		with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5) as ser:
			print("<sensors.py> [INFO] Waiting for data...")
			while True: 
				line = ser.readline().decode("utf-8", errors="replace").strip()
				if line: 
					# print(f"[INFO] Received: {line}")
					sensor_data = parse_data(line)
					logger.log_data(sensor_data)
	except serial.SerialException as e: 
		print(f"<sensors.py> [ERROR] Serial connection issue: {e}")
		logger.close_logger()
	except KeyboardInterrupt: 
		print("<sensors.py> [INFO] Stopping sensor read.")
		logger.close_logger()

def parse_data(raw_line): 
	global gps_buffer

	try: 
		data = [float(x) for x in raw_line.split(", ")]
		if len(data) > 10:
			gps_buffer = data[10:15]
			print(f"[DEBUG] GPS_buffer: {gps_buffer}")

		return data

	except ValueError: 
		print(f"<sensors.py> [WARNING] Invalid data format: {raw_line}")
		return []

def send_data(): 
	global sensor_data
	global gps_buffer
	
	last_sent_time = time.time()

	# define packet contents (hardcoded) col1 sensor index, col2 packet no. 
	packet_matrix = [
		(0, 1), (1, 1), (2, 1), (3, 1), 
		(4, 2), (5, 2), (6, 2), 
		(7, 3), (8, 3), (9, 3), 
		(10, 4), (11, 4), (12, 4), 
		(13, 5), (14, 5), 
	]

	while True: 
		current_time = time.time()
		if current_time - last_sent_time >= 1.0:
			sensor_data_upd = sensor_data[:] if len(sensor_data) > 0 else []
			if len(sensor_data_upd) <= 10: 
				sensor_data_upd += gps_buffer

			packet_data = {}
			for index, packet_no in packet_matrix: 
				if index < len(sensor_data_upd):
					if packet_no not in packet_data: 
						packet_data[packet_no] = []
					packet_data[packet_no].append(sensor_data_upd[index])

			for packet_no, data in packet_data.items():
				#format packet
				RF_line = f"{packet_no:02d}," + ','.join(map(str, data))
				print(f"<sensors.py> [RF] Sending telemetry: {RF_line}")
				transceiver.send_telemetry(RF_line)

				time.sleep(0.05)

			last_sent_time = current_time

		time.sleep(0.01)

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

