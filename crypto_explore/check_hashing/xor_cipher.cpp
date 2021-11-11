#include <bits/stdc++.h>
using namespace std;
typedef long long LL;
const LL MOD = 1000000007;
#define pb push_back
#define all(c) (c).begin(), (c).end()
#define debug(x) cout << #x << " : " << x << endl
#define part cout << "----------------------------------\n";
#include <iostream>

int dx[] = {1, 1, 0, -1, -1, -1, 0, 1}; // trick to explore an implicit 2D grid
int dy[] = {0, 1, 1, 1, 0, -1, -1, -1}; // S,SE,E,NE,N,NW,W,SW neighbors  //GO FOR EVEN FOR 4 moves

#define fastinput                     \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);

LL POW(LL x, LL y, LL mod_give)
{
    LL ans = 1;
    LL base = x;
    while (y)
    {
        if (y & 1)
        {
            ans *= base;
            ans %= mod_give;
        }
        base = base * base;
        base %= mod_give;
        y = y >> 1;
    }
    return ans;
}

string XOR_KEY = "PQRST";
int rand_master = 12;
int rand_num = 0;
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
        int want=((rand_num + x) % 256) ^ XOR_KEY[idx];
        // cout<<((rand_num + x) % 256)<<" ^ "<<int(XOR_KEY[idx])<<"="<<want<<endl;
        // debug(want);
        // cout<<x<<" "<<want<<endl;
        ans += char(want);
    }
    return ans;
}
int main()
{
    fastinput;
    LL n, i, j, k, t, temp, tc;
    string s;
    s="1234567890";
    // cin >> s;
    string encrypted_version = encrypt_string(s);
    // debug(encrypted_version);
    // debug(encrypt_string(encrypted_version));
    cout << encrypted_version;
    return 0;
}
