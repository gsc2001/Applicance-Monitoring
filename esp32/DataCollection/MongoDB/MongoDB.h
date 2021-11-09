#include <bits/stdc++.h>
#include <WiFi.h>

class MongoDB
{
    String device;
    String sender;
    int version;
    int delay;
    String description;
    int iteration;
    int zeroValue;
    std::vector<int> dataPoints;
    int dumpToServer();

public:
    MongoDB(String device, String sender, int version, int delay, String description);
    void setZeroValue(int value);
    int pushData(int data);
};