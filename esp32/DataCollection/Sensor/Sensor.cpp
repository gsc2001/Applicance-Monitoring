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
  pinMode(2, OUTPUT);
  Serial.println("Press button");
  touchAttachInterrupt(TOUCH_PIN, deviceConnected, 40);
  // Increase 40 to increase touch sensitivity and vice-versa
  // Refer to the numbers printing in the Serial Monitor to find the best touch sensitivity
  isDeviceConnected = false;
  digitalWrite(2, HIGH);
  while (!isDeviceConnected)
  {
    // Serial.println("Press BUTTON");
    Serial.println(touchRead(TOUCH_PIN));
    delay(5000);
  }
  digitalWrite(2, LOW);
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
    float read_value = analogRead(this->pin);
    readings[i] = (3.3 * read_value) / 4096;
    // Serial.println("Partition Read value is ");
    // Serial.println(read_value);
    // Serial.println("Voltage read is ");
    // Serial.println(readings[i]);
    // delay(10*gapMilis);
    delay(gapMilis);
  }
  return readings;
}

float Sensor::getData()
{
  float reading = this->read(1, 0)[0];
  // Serial.println("Voltage read is ");
  // Serial.println(reading);

  reading -= this->zeroValue;
  // Serial.println("Zero value is ");
  // Serial.println(this->zeroValue);
  reading /= this->sensitivity;
  // Serial.println("SENSE is ");
  // Serial.println(this->sensitivity);
  // Serial.println("Current predicted is ");
  // Serial.println(reading);

  return reading;
}

float Sensor::getZeroValue()
{
  Serial.println("Finding Zero Value");
  float zero = 0;
  for (int i = 0; i < 3; i++)
  {
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
  Serial.println("Zero Value (voltage) = " + String(zero));
  return zero;
}

float Sensor::getSensitivity(float current)
{
  Serial.println("Finding Sensitivity. Make sure zero value was initialized.");
  auto readings = read(1000, 2);

  float vrms2 = 0;

  for (float reading : readings)
    vrms2 += pow(reading - this->zeroValue, 2);

  vrms2 /= 1000;
  Serial.println("vrms read is ");
  Serial.println(vrms2);

  float sensitivity = sqrt(vrms2) / current;
  Serial.println("Sensitivity = " + String(sensitivity));
  return sensitivity;
}

void Sensor::init()
{
  Serial.println("Initializing Sensor...");
  this->zeroValue = this->getZeroValue();
  Serial.println("Zero value fetched as ");
  Serial.println(this->zeroValue);

  Serial.println("Now will wait for PRESSING BLUE LIGHT button");
  waitForDeviceConnected();
  Serial.println("Device connected ...");

  // Uncomment for getting sensitivity
  // Serial.println("Getting sensitivity...");
  // Serial.println(this->getSensitivity(1200 / 220.0)); // Replace 1200 with device power in Watts
}
