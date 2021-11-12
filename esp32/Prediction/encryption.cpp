#include <bits/stdc++.h>
using namespace std;

String XOR_KEY = "AB12:>";
int rand_master = 12;
int rand_num = 0;

String encrypt_string(String s)
{
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

// void populate_stuff()
// {
//     // int lb=44;
//     // int ub=44+64-1;
//     for (int i = 0; i < 64; i++)
//     {
//         char now = (char)(i + 44);
//         char_to_ascii[now] = i;
//         ascii_to_char[i] = now;
//     }
// }
// int main()
// {
//     string s;
//     s = "01,23,456,789a,bcwfwe";
//     string encrypted_version = encrypt_string(s);
//     cout << encrypted_version;
//     return 0;
// }
