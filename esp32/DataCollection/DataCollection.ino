#include <WiFi.h>
#include "MongoDB/MongoDB.cpp"
#include "Sensor/Sensor.cpp"
#include "secrets.h"
#define DELAY 10 // 10 data points in each second

bool error = false;

MongoDB server("HD", "Anmol", 10, DELAY, "7th Dec, 9:15pm time");
/*
First param ("T"): Device name
                      T: Testing
                      WM: Washing Machine
                      HD: Hair Dryer
                      MW: Microwave
                      IR: Iron
                      VC: Vaccum Cleaner
Second param ("Sanchit"): Sender name
Third param (1): Version of the data for same device, by same sender
Fourth param (DELAY): MUST NOT CHANGE!
Fifth param ("9th Nov ~4pm"): Anything else you want to store in the database, date and approx time is compulsory
*/

Sensor sensor(35,0.02); // change 1 to actual sensitivity

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

  //we want to connect to wifi, will retry again and again
  connectToWiFi();


  sensor.init();

  //multupy by 1000 and send
  server.setZeroValue(sensor.getZeroValue() * VALUE_MULTIPLIER);
}

// Comment everything in loop() when calculating sensitivity
void loop()
{
  //wait for wifi to get connected
  connectToWiFi();

  for (int i = 0; i < MAX_POINTS && !error; i++)
  {
    //psuhData works only when MAX_POINTS has been colllected
    //separatation between any 2 instances for 100 data points per seconds is 10, so delay should be 10 sec
    if (server.pushData(sensor.getData() * VALUE_MULTIPLIER))
    {
      Serial.println("ERROR: Wrong configuration");
      Serial.println("Breaking out of loop. Please restart with correct configuration.");
      error = true;
    }

    delay(DELAY);
  }
}
