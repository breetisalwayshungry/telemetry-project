#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_MPU6050.h>
#include <AltSoftSerial.h>
#include <TinyGPS.h>

// Initialize TX RX
AltSoftSerial gpsSerial; // 8 RX 9 TX
TinyGPS gps; 

// Create BMP280 object
Adafruit_BMP280 bmp;

// Create MPU6050 object
Adafruit_MPU6050 mpu;

// Create global variables to store sensor data
// BMP280
float temperature = 0.0; // C
float pressure = 0.0; // kPa
float altitude = 0.0; // m

// MPU6050
float ax = 0.0; // g (9.81 m/s/s)
float ay = 0.0; 
float az = 0.0; 
float gx = 0.0; // deg/s
float gy = 0.0; 
float gz = 0.0; 

// GPS
float lat = 0.0; 
float lon = 0.0; 
float gps_alt = 0.0; 
float speed = 0.0; // m/s
int sat_count = 0; 

unsigned long lastSensorUpdate = 0; 
unsigned long sensorInterval = 25; // Sensor data output every 25ms (40Hz)
bool printGPSData = false; 

void setup() {
  Serial.begin(115200); // Start the serial communication
  gpsSerial.begin(9600); // GPS module baud rate
  Wire.begin();

  // Serial.println("Initializing GPS and Sensor System..."); 

  bmp.begin(0x76); // Initialize the BMP280 sensor
  mpu.begin(0x68); // Initialize the MPU6050 sensor

  // Optional: Set the sensor’s parameters
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,  // Operating Mode
                  Adafruit_BMP280::SAMPLING_X1,  // Temp oversampling
                  Adafruit_BMP280::SAMPLING_X1,  // Pressure oversampling
                  Adafruit_BMP280::FILTER_OFF,   // Filtering
                  Adafruit_BMP280::STANDBY_MS_125);  // Standby time

  // Set accelerometer range to ±16g 
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);

  // Set gyroscope range to ±500°/s 
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  // Set the filter bandwidth to 21 Hz
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Display sensor initialization message
  // Serial.println("Flight Arduino initialized!");
}

void loop() {
  // GPS Data
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    if (gps.encode(c)) {
      gps.f_get_position(&lat, &lon);
      gps_alt = gps.f_altitude();
      sat_count = gps.satellites();
      speed = gps.speed() / 1.94384; // knots to m/s
      printGPSData = true; 
    }
  }

  // Handle Sensor Data Output (every 'sensorInterval' ms)
  if (millis() - lastSensorUpdate >= sensorInterval) {
    // Simulate sensor data 
    temperature = bmp.readTemperature(); 
    pressure = bmp.readPressure() / 1000; 
    altitude = bmp.readAltitude(1013.25); 
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);  // Get accelerometer (a), gyroscope (g)
    ax = a.acceleration.x; 
    ay = a.acceleration.y; 
    az = a.acceleration.z; 
    gx = g.gyro.x; 
    gy = g.gyro.y; 
    gz = g.gyro.z; 
    
    // Output data via Serial
    Serial.print(millis()); 
    Serial.print(", "); 
    Serial.print(temperature); 
    Serial.print(", ");
    Serial.print(pressure);
    Serial.print(", ");
    Serial.print(altitude);
    Serial.print(", "); 
    Serial.print(ax);
    Serial.print(", ");
    Serial.print(ay); 
    Serial.print(", ");
    Serial.print(az); 
    Serial.print(", ");
    Serial.print(gx);
    Serial.print(", ");
    Serial.print(gy); 
    Serial.print(", ");
    Serial.print(gz); 

    // If GPS data is ready, output GPS data as well
    if (printGPSData) {  // If GPS data was updated recently
      Serial.print(", ");
      Serial.print(lat, 6);
      Serial.print(", ");
      Serial.print(lon, 6);
      Serial.print(", "); 
      Serial.print(gps_alt, 2);
      Serial.print(", "); 
      Serial.print(speed, 2); 
      Serial.print(", "); 
      Serial.print(sat_count);

      printGPSData = false; 
    }
    
    Serial.println(); 
    lastSensorUpdate = millis();  // Update the last sensor update time
  }
}
