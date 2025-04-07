import time
from pyrf24 import RF24, RF24_PA_HIGH, RF24_250KBPS

# Initialie radio
radio = RF24(5, 0) # GPIO 5 is CE pin, GPIO 8 is CSN pin 0

# Set up pipes for telemetry and ground commands
TELEM_PIPE = b'00001' # match to ground arduino
COMMD_PIPE = b'00002'

def setup_radio():
	radio.begin()
	radio.setPALevel(RF24_PA_HIGH)
	radio.setDataRate(RF24_250KBPS) # fastest rate (2Mbps). lower to increase range
	radio.setChannel(0x4c) # again, match to arduino
	radio.openWritingPipe(TELEM_PIPE)
	radio.openReadingPipe(1, COMMD_PIPE)
	radio.setAutoAck(False) # disable acknowledgements
	radio.startListening()

def send_telemetry(message="test"): # default 'test' if no message passed
	radio.stopListening()

	success = radio.write(message.encode('utf-8'))
	if success: 
		print(f"<transceiver.py> [RF] Sent: {message}")

	radio.startListening()

def receive_command(): 
	if radio.available(): 
		command = radio.read(radio.getDynamicPayloadSize()).decode('utf-8')
		print(f"<transceiver.py> [RF] Command received: {command}")
		process_command(command)

def process_command(command):
	if command == "TEST": 
		print("<transceiver.py> [INFO] Test Successful")
	elif command == "example": 
		# perform action
		print("<transceiver.py> [INFO] this is an example")
	else: 
		print(f"<transceiver.py> [WARNING] Unknown command: {command}")

if __name__ == "__main__":
	setup_radio()
	
	while True: # for testing/debugging
		send_telemetry()
		time.sleep(1)
		receive_command()

