#include <WiFi.h>
#include "MongoDB/MongoDB.cpp"
#include "Sensor/Sensor.cpp"
#include "secrets.h"

MongoDB server;

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

  Sensor sensor(35, 1); // change 1 to actual sensitivity
  sensor.init();
}

void loop()
{
  // connectToWiFi();
  // for (int i = 0; i <= MAX_POINTS; i++)
  //   server.pushData("testf", 10 * 10000);
  // Serial.println("hi");
  // delay(2000);
}
