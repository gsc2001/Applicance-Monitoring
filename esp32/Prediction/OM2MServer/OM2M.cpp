#include <bits/stdc++.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include "OM2M.h"
#include "../secrets.h"
#include "../config.h"

String XOR_KEY = "AB12:>";
int rand_master = 12;
int rand_num = 0;

String encrypt_string(String s)
{
    // return s;
    int idx = -1;
    int key_len = XOR_KEY.length();
    String ans = "";
    for (auto &x : s)
    {
        rand_num += 1;
        rand_num %= rand_master;
        idx += 1;
        idx %= key_len;
        int want = ((rand_num + (x - 44)) % 64) ^ (XOR_KEY[idx] - 44);
        ans += want + 44;
    }
    return ans;
}

// char *key = "abcdefghijklmnop";
// unsigned char output[100];
// char input[100];

// String encrypt_block(String inp)
// {

//     inp.toCharArray(input, inp.length() + 10);

//     mbedtls_aes_context aes;
//     mbedtls_aes_init(&aes);
//     mbedtls_aes_setkey_enc(&aes, (const unsigned char *)key, strlen(key) * 8);
//     mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_ENCRYPT, (const unsigned char *)input, output);
//     mbedtls_aes_free(&aes);
//     String out = "";
//     for (int i = 0; i < 16; i++)
//     {
//         char str[3];
//         sprintf(str, "%02x", (int)output[i]);
//         out += String(str);
//     }

//     // Serial.println(out);
//     return out;
// }

// String encrypt(String s)
// {
//     while (s.length() % 16 != 0)
//     {
//         s += " ";
//     }

//     String encrypted = "";
//     for (int i = 0; i < s.length(); i += 16)
//     {
//         encrypted += encrypt_block(s.substring(i, i + 16));
//     }

//     // Serial.println("Encrypted");
//     // Serial.println(encrypted);
//     return encrypted;
// }

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
    Serial.println(dataStr);
    dataStr = encrypt_string(dataStr);
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
