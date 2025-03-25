import serial
import time
import csv

class ArduinoReader:
    def __init__(self, port='COM7', baud_rate=9600, output_file='telemetry_data.csv'):
        """Initialize serial connection and CSV file."""
        self.port = port
        self.baud_rate = baud_rate
        self.output_file = output_file
        self.ser = None

        # Attempt to connect to the serial port
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Allow time for connection to establish
            print(f"Connected to {self.port} at {self.baud_rate} baud.")
        except serial.SerialException as e:
            print(f"Error: {e}")
            exit(1)

        # Open CSV file and write headers if new
        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If file is empty, write header
                writer.writerow(['Timestamp', 'Message'])

    def read_telemetry(self):
        """Reads and writes data from Arduino to CSV file."""
        try:
            with open(self.output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                while True:
                    if self.ser.in_waiting > 0:
                        telemetry_data = self.ser.readline().decode('utf-8').strip() # get data
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                        # Check if the telemetry data contains commas
                        if ',' in telemetry_data:
                            # If it contains commas, split by commas and write each part as a separate column
                            split_data = telemetry_data.split(',')
                            row_data = [timestamp] + split_data  # Add timestamp at the beginning
                        else:
                             # If no commas, treat it as one data entry and write it as a single value
                             row_data = [timestamp, telemetry_data]
                        
                        writer.writerow([timestamp, telemetry_data])
                        print(f"{timestamp}: {telemetry_data}")

        except KeyboardInterrupt:
            print("\nStopping data collection...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close()

    def close(self):
        """Closes the serial connection gracefully."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Closed connection to {self.port}")

# Run the reader
if __name__ == "__main__":
    output_file = f"C:/Users/kingf/OneDrive/Documents/Arduino/telemproject_ground_arduino/data/telemetry_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    reader = ArduinoReader(output_file=output_file)
    reader.read_telemetry()
