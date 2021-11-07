#include <bits/stdc++.h>
#include <WiFi.h>

class MongoDB
{
    String lastConnectedDevice;
    String sender;
    String description;
    int zeroValue;
    std::vector<int> dataPoints;
    void dumpToServer();

public:
    MongoDB(String sender, String description);
    void setZeroValue(int value);
    void pushData(String device, int data);
};