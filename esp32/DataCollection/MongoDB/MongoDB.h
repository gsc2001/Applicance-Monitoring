#include <bits/stdc++.h>
#include <WiFi.h>

class MongoDB
{
    String lastConnectedDevice;
    std::vector<int> dataPoints;
    void dumpToServer();

public:
    MongoDB();
    void pushData(String device, int data);
};