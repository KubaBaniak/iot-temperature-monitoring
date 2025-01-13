#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "secrets.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>

#define DHTPIN 5
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

unsigned long lastTime = 0;
unsigned long timerDelay = 600000;

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  dht.begin();
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
  randomSeed(analogRead(0));
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;
      
      float temperature = dht.readTemperature();
      float humidity = dht.readHumidity();

      if (!isnan(temperature) && !isnan(humidity)) {
        Serial.println("Temperature: " + String(temperature));
        Serial.println("Humidity: " + String(humidity));
        
        http.begin(client, serverName);

        http.addHeader("Content-Type", "application/json");

        String jsonPayload = "{\"temperature\": " + String(temperature, 2) + ", \"humidity\": " + String(humidity, 2) + "}";
        int httpResponseCode = http.POST(jsonPayload);

        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);

        http.end();
      } else {
        Serial.println("Failed to read from DHT sensor. Skipping data send.");
      }
    } else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}


