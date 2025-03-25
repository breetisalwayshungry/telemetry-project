# telemetry-project
Contains the code for an Arduino/Raspberry Pi based telemetry system, used in amateur rocketry. Designed, built, and integrated entirely by yours truly. 

The overall system architecture is comprised of two interactive components - ground and flight. 

The ground component operates as a receiver (though capable of sending commands for future use): 
* ground_arduino.ino - ground transceiver code. Interprets transmitted telemetry from flight system.
* telemetry_io.py - OOP code to read serial data from ground_arduino.ino and put data in csv.

The flight component reads, writes, and transmits data: 
* start_telem.sh - automation script to start camera and sensor code. Executed on startup.
* telemproj.service - enables Pi to run start_telem.sh on startup.
* sensors.py - script to read sensor data from serial input, delegates to transceiver.py and logger.py to transmit/log data.
* transceiver.py - sends and receives messages at a defined rate (1Hz). For this current implementation, it will only send messages - though it is built to accept commands as well.
* logger.py - saves flight data to CSV at a much higher rate than what is transmitted. To reduce fatigue on the disk, data is saved to a buffer before batch saving.
* flight_arduino.ino - communicates with peripherals (sensors) and organizes returned data into preferred format.
