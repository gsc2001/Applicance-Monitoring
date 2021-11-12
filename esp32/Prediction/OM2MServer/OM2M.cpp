#include <bits/stdc++.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include "OM2M.h"
#include "../secrets.h"
#include "../config.h"
#include "../encryption.cpp"

int OM2M::init(int delay)
{
    this->delay = delay;
}

int OM2M::dumpToServer()
{
    Serial.println("Dumping");

    HTTPClient http;

    http.begin(OM2M_SERVER);
    http.addHeader("Content-Type", "application/json;ty=4");
    http.addHeader("X-M2M-Origin", "admin:admin");
    String dataStr = String(this->delay) + ",";

    reverse(this->dataPoints.begin(), this->dataPoints.end());
    while (this->dataPoints.size())
    {
        dataStr += String(this->dataPoints.back());

        this->dataPoints.pop_back();
        if (this->dataPoints.size())
            dataStr += ",";
    }
    dataStr = encrypt_string(dataStr);
    Serial.println(dataStr);
    String JSONstr = String("{ \"m2m:cin\": {\"con\":");
    // Serial.println(JSONstr);
    JSONstr += String("\"" + dataStr + "\"");
    // Serial.println(JSONstr);
    JSONstr += "} }";
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

    return 0;
}

int OM2M::pushData(int data)
{
    this->dataPoints.push_back(data);
    // Serial.println(dataPoints.size());
    if (this->dataPoints.size() == MAX_POINTS)
        return this->dumpToServer();

    return 0;
}
