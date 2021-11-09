#include <bits/stdc++.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include "MongoDB.h"
#include "../secrets.h"
#include "../config.h"

MongoDB::MongoDB(String device, String sender, int version, int delay, String description = "")
{
    this->device = device;
    this->sender = sender;
    this->version = version;
    this->delay = delay;
    this->description = description;
    this->dataPoints = {};
    this->iteration = 0;
}

int MongoDB::dumpToServer()
{
    Serial.println("Dumping");

    HTTPClient http;

    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    String JSONstr = String("{")                                               //
                     + "\"device\": " + "\"" + this->device + "\", "           //
                     + "\"sender\": " + "\"" + this->sender + "\", "           //
                     + "\"version\": " + this->version + ", "                  //
                     + "\"delay\": " + this->delay + ", "                      //
                     + "\"description\": " + "\"" + this->description + "\", " //
                     + "\"iteration\": " + this->iteration + ", "              //
                     + "\"zeroValue\": " + this->zeroValue + ", "              //
                     + "\"data\": [";

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

    if (statusCode == HTTP_CODE_OK)
        Serial.println("Success");
    else if (statusCode == HTTP_CODE_CONFLICT)
    {
        Serial.println("Datapoints with the same quadruple (device, sender, version, iteration) exists. Can't overwrite.");
        return 1;
    }
    else
        Serial.println(http.errorToString(statusCode).c_str());

    this->iteration++;

    return 0;
}

void MongoDB::setZeroValue(int value)
{
    this->zeroValue = value;
}

int MongoDB::pushData(int data)
{
    this->dataPoints.push_back(data);

    if (this->dataPoints.size() == MAX_POINTS)
        return this->dumpToServer();

    return 0;
}
