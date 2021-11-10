#include <bits/stdc++.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino.h>
#include <time.h>

class OM2M
{
    int delay;
    // int iteration;
    std::vector<int> dataPoints;
    int dumpToServer();

public:
    int pushData(int data);
    int init(int delay);
};