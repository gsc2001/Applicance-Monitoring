#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
const LL MOD = 1000000007;
#define pb push_back
#define all(c) (c).begin(), (c).end()
#define debug(x) cout << #x << " : " << x << endl
#define part cout << "----------------------------------\n";
#include <iostream>

#define fastinput                     \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

string XOR_KEY = "AB12:>";
int rand_master = 12;
int rand_num = 0;

unordered_map<char, int> char_to_ascii;
unordered_map<int, char> ascii_to_char;
string encrypt_string(string s)
{
    int idx = -1;
    int key_len = XOR_KEY.length();
    string ans = "";
    for (auto &x : s)
    {
        rand_num += 1;
        rand_num %= rand_master;
        idx += 1;
        idx %= key_len;
        // debug(int(XOR_KEY[idx]));
        int want = ((rand_num + char_to_ascii[x]) % 64) ^ char_to_ascii[XOR_KEY[idx]];
        // cout<<((rand_num + x) % 256)<<" ^ "<<int(XOR_KEY[idx])<<"="<<want<<endl;
        // debug(want);
        // cout<<x<<" "<<want<<endl;
        // cout << "char is " << char(want) << endl;
        ans += ascii_to_char[want];
    }
    return ans;
}

void populate_stuff()
{
    // int lb=44;
    // int ub=44+64-1;
    for (int i = 0; i < 64; i++)
    {
        char now = (char)(i + 44);
        char_to_ascii[now] = i;
        ascii_to_char[i] = now;
    }
}
int main()
{
    fastinput;

    //#################
    populate_stuff();
    //#################
    LL n, i, j, k, t, temp, tc;
    string s;
    s = "01,23,456,789a,bcwfwe";
    // cin >> s;
    string encrypted_version = encrypt_string(s);
    // debug(encrypted_version);
    // debug(encrypted_version.length());
    // debug(encrypt_string(encrypted_version));
    cout << encrypted_version;
    return 0;
}
