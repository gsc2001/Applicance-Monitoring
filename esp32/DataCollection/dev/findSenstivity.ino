#include <WiFi.h>
#include <ThingSpeak.h>
#include "../Sensor/Sensor.h"
#include "../config.h"

// senstivity 0 for now
Sensor sensor(SENSOR_PIN, 0);

void setup()
{
    Serial.begin(115200);
    sensor.init();
    // put your setup code here, to run once:
}

void loop()
{
    // put your current below;
    float senstivity = sensor.getSensitivity(10);
    Serial.println(senstivity);
}
