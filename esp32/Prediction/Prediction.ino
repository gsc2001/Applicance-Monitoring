#include "OM2MServer/OM2M.cpp"
#include "Sensor/Sensor.cpp"
#include "secrets.h"
#include "config.h"
#define DELAY 10

OM2M server;
Sensor sensor(35, 0.03);

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
    Serial.println("Start");
    connectToWiFi();
    sensor.init();
    server.init(DELAY);
}

void loop()
{
    connectToWiFi();
    bool error = false;

    for (int i = 0; i < MAX_POINTS && !error; i++)
    {
        float rec_data = sensor.getData();
        //Serial.println(rec_data);
        if (server.pushData(rec_data * VALUE_MULTIPLIER))
        {
            Serial.println("ERROR: Wrong configuration");
            Serial.println("Breaking out of loop. Please restart with correct configuration.");
            error = true;
        }

        delay(DELAY);
    }
}
