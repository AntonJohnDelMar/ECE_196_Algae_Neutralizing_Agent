#include <WiFi.h>
#include <ESP32Servo.h> 

// Check .env 
const char* theSSID { "" }; 
const char* thePassword { "" }; 

const int serverPort { 0 }; // Check .env 
WiFiServer theServer(serverPort); 

const int LED1 { 17 }; 
const int LED2 { 18 }; 
const int theServoPin { 21 }; 
const int theOffset { 0 }; 
Servo theServo; 

void setup() { 
  pinMode(LED1, OUTPUT); 
  pinMode(LED2, OUTPUT); 
  theServo.attach(theServoPin); 
  delay(500); 
  theServo.write(90 + theOffset); 
  delay(500); 

  Serial.begin(9600); 
  WiFi.softAP(theSSID, thePassword); 
  delay(500); 

  Serial.println("ESP32 IP: "); 
  Serial.println(WiFi.softAPIP()); 
  Serial.println(); 

  theServer.begin(); 
} 

void loop() {
  delay(1000); 

  WiFiClient theClient = theServer.available();  

  if(theClient) { 
  Serial.println("Client connected."); 
    while(theClient.connected()) {
        if(theClient.available()) {
          int theReceived = theClient.readString().toInt(); 
          // theClient.write(theReceived); 
          // Serial.println(theReceived); 
          theServo.write(theReceived); 
          // delay(1000); 
        }
    }
  Serial.println("Client disconnected."); 
  }
  theClient.stop(); 
} 
