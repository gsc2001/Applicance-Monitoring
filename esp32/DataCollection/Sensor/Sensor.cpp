#include <bits/stdc++.h>
#include <Arduino.h>
#include "Sensor.h"

Sensor::Sensor(int pin, float senstivity)
{
  this->pin = pin;
  this->senstivity = senstivity;
  this->zeroValue = 0;
}

std::vector<float> Sensor::read(int iters, int gapMilis)
{
  std::vector<float> readings(iters);
  for (int i = 0; i < iters; i++)
  {
    readings[i] = analogRead(this->pin);
    delay(gapMilis);
  }
  return readings;
}

float Sensor::getZeroValue()
{
  Serial.println("Finding Zero Value");
  float zero = 0;
  for (int i = 0; i < 3; i++)
  {
    float avg_reading = 0;
    auto readings = read(500, 2);
    float avg_reading = 0;
    for (auto r : readings)
      avg_reading += r;
    avg_reading /= 500;
    zero += avg_reading;
    Serial.print(".");
    delay(500);
  }

  Serial.println("Done");
  zero /= 3;
  Serial.println("Zero Value = " + String(zero));
  return zero;
}

void Sensor::init()
{
  if (!Serial.available())
    Serial.begin(115200);
  Serial.println("Initializing Sensor...");
  this->zeroValue = this->getZeroValue();
  Serial.println("Connect Device and enter `done`");
  String _data = Serial.readStringUntil('\r\n');
  if (_data == "done")
    Serial.println("Initialization Done");
  else
  {
    Serial.println("Initialization Failed!");
    exit(1);
  }
}
