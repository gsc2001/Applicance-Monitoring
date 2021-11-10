#include <WiFi.h>
#include "MongoDB/MongoDB.cpp"
#include "Sensor/Sensor.cpp"
#include "secrets.h"
#define DELAY 10 // 100 data points in each second

bool error = false;

MongoDB server("EK", "Anmol", 1, DELAY, "Electric Kettle first attempt 4PM Nov 10");
/*
First param ("T"): Device name
                      T: Testing
                      WM: Washing Machine
                      HD: Hair Dryer
                      MW: Microwave
                      IR: Iron
                      VC: Vaccum Cleaner
                      MG: Mixer grinder
                      EK: ELectric Kettle
Second param ("Sanchit"): Sender name
Third param (1): Version of the data for same device, by same sender
Fourth param (DELAY): MUST NOT CHANGE!
Fifth param ("9th Nov ~4pm"): Anything else you want to store in the database, date and approx time is compulsory
*/

Sensor sensor(35, 0.03); // change 1 to actual sensitivity

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
  Serial.println("Inside setup, before WiFi is tried to be connected");

  connectToWiFi();
  //return;

  sensor.init();
  Serial.println("Server zero value set trying");
  server.setZeroValue(sensor.zeroValue * VALUE_MULTIPLIER);
}

// Comment everything in loop() when calculating sensitivity
void loop()
{
  //return;
  // Serial.println("Entered loop");
  // Serial.println("Zero val ie current when nothing is passed is ");
  // Serial.println(sensor.zeroValue);
  // // connectToWiFi();

  // float current_passed = 1000.0 / 220;
  // Serial.println("Current passed is ");
  // Serial.println(current_passed);
  // float senstivity = sensor.getSensitivity(current_passed);
  // Serial.println("Sensitivity is (dV/DI)");
  // Serial.println(senstivity);
  // return;
  // waitForDeviceConnected();

  for (int i = 0; i < MAX_POINTS && !error; i++)
  {
    if (server.pushData(sensor.getData() * VALUE_MULTIPLIER))
    {
      Serial.println("ERROR: Wrong configuration");
      Serial.println("Breaking out of loop. Please restart with correct configuration.");
      error = true;
    }
    // Serial.println("Current passed is ");
    // Serial.println(current_passed);
    // float senstivity = sensor.getSensitivity(current_passed);
    // Serial.println("Sensitivity is (dV/DI)");
    // Serial.println(senstivity);
    // Serial.println("###########################");

    delay(DELAY);
  }
}
