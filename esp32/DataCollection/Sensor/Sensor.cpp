#include <bits/stdc++.h>
#include <Arduino.h>
#include "Sensor.h"
#include "../config.h"
#define TOUCH_PIN T0

bool isDeviceConnected = false;

void deviceConnected()
{
  isDeviceConnected = true;
}

void waitForDeviceConnected()
{
  touchAttachInterrupt(TOUCH_PIN, deviceConnected, 40);

  while (!isDeviceConnected)
    delay(1000);
}

Sensor::Sensor(int pin, float sensitivity)
{
  this->pin = pin;
  this->sensitivity = sensitivity;
  this->zeroValue = 0;
}

std::vector<float> Sensor::read(int iters, int gapMilis)
{
  std::vector<float> readings(iters);
  for (int i = 0; i < iters; i++)
  {
    readings[i] = 3.3 * analogRead(this->pin) / 4096;
    delay(gapMilis);
  }
  return readings;
}

int Sensor::getData()
{
  float reading = this->read(1, 0)[0];
  reading -= this->zeroValue;
  reading /= this->sensitivity;
  reading *= 10000;

  return reading;
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

float Sensor::getSensitivity(float current)
{
  Serial.println("Finding Sensitivity. Make sure zero value was initialized.");
  auto readings = read(1000, 2);

  float vrms2 = 0;

  for (float reading : readings)
    vrms2 += pow(reading - this->zeroValue, 2);

  vrms2 /= 500;

  return sqrt(vrms2) / current;
}

void Sensor::init()
{
  if (!Serial.available())
    Serial.begin(115200);
  Serial.println("Initializing Sensor...");
  this->zeroValue = this->getZeroValue();
  waitForDeviceConnected();
  Serial.println("Device connected ...");
}
