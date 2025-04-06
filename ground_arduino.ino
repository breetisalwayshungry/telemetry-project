#include <SPI.h>
#include <RF24.h>

// Define the pins for the NRF24L01+ module
#define CE_PIN   8
#define CSN_PIN  9

// Create an RF24 object
RF24 radio(CE_PIN, CSN_PIN);

// Define the address for communication (must match on both receiver and transmitter)
byte telemPipe[6] = "00001";
byte commandPipe[6] = "00002"; 

void setup() {
  // Start the serial communication
  Serial.begin(9600);
  
  // Initialize the NRF24L01+ radio
  radio.begin();
  
  // Set the channel and data rate 
  radio.setChannel(0x4c);   // Set channel to 76 (can be adjusted)
  radio.setPALevel(RF24_PA_HIGH);  // Set power amplifier level
  radio.setDataRate(RF24_250KBPS);   // Set data rate 
  
  // Open the pipes
  radio.openReadingPipe(1, telemPipe);
  radio.openWritingPipe(commandPipe); 

  // Disable auto acknowledge (needs to be same for both receiver and sender)
  radio.setAutoAck(false); 
  
  // Start listening for incoming data
  radio.startListening();
  
  Serial.println("Receiver is ready to receive data...");
}

void loop() {
  // Check if data is available to read
  if (radio.available()) {
    char receivedMessage[64] = "";  // Buffer to hold the received message
    radio.read(&receivedMessage, sizeof(receivedMessage));  // Read data into buffer
    
    Serial.print("Received: ");
    Serial.print(receivedMessage);
    }
    delay(10); 
  }
}
