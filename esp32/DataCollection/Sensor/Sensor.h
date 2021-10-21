#include <bits/stdc++.h>

class Sensor
{
public:
    int pin;
    float sensitivity, zeroValue;
    Sensor(int pin, float senstivity);
    void init();
    std::vector<float> read(int iters = 500, int gapMilis = 2);
    float getZeroValue();
    float getSensitivity(float current);
    float readAverage(float offset = 0, int iters = 500);
    float readRMS();
};