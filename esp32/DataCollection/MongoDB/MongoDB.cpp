#include <bits/stdc++.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include "MongoDB.h"
#include "../secrets.h"
#include "../config.h"

MongoDB::MongoDB()
{
    this->lastConnectedDevice = "";
    this->dataPoints = {};
}

void MongoDB::dumpToServer()
{
    if (this->lastConnectedDevice.length() == 0)
        return;

    Serial.println("Dumping");

    HTTPClient http;

    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    String JSONstr = "{\"device\": \"" + this->lastConnectedDevice + "\", \"data\": [";

    reverse(this->dataPoints.begin(), this->dataPoints.end());
    while (this->dataPoints.size())
    {
        JSONstr += String(this->dataPoints.back());

        this->dataPoints.pop_back();
        if (this->dataPoints.size())
            JSONstr += ",";
    }

    JSONstr += "] }";

    // Serial.println(JSONstr);

    int statusCode = http.POST(JSONstr);

    Serial.println(statusCode);
    // Serial.println(http.errorToString(statusCode).c_str());

    this->lastConnectedDevice = "";
}

void MongoDB::pushData(String device, int data)
{
    if (device != this->lastConnectedDevice)
        this->dumpToServer();

    this->lastConnectedDevice = device;
    this->dataPoints.push_back(data);

    // if (this->dataPoints.size() % 1000)
    //     Serial.println(this->dataPoints.size());

    if (this->dataPoints.size() == MAX_POINTS)
        this->dumpToServer();
}
