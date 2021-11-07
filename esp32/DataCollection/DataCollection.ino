#include <WiFi.h>
#include "MongoDB/MongoDB.cpp"
#include "Sensor/Sensor.cpp"
#include "secrets.h"

MongoDB server("Sanchit");
Sensor sensor(35, 1); // change 1 to actual sensitivity

void connectToWiFi()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
      WiFi.begin(SSID, PASS);
      Serial.println('.');
      delay(5000);
    }
    Serial.println("Connected to WiFi");
  }
}

void setup()
{
  Serial.begin(115200);
  delay(5000);

  connectToWiFi();

  sensor.init();
  server.setZeroValue(sensor.getZeroValue() * VALUE_MULTIPLIER);
}

void loop()
{
  connectToWiFi();

  for (int i = 0; i < MAX_POINTS; i++)
  {
    server.pushData("test", sensor.getData() * VALUE_MULTIPLIER);
    delay(100); // 10 points in each second
  }
}
