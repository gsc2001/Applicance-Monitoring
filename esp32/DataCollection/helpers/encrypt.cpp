#include <tinyECC.h>

String encrypt(String data)
{
    tinyECC e;
    e.plaintext = data;
    e.encrypt();
    return e.ciphertext;
}

String encrypt(int data)
{
    return encrypt(String(data));
}

String decrypt(String data)
{
    tinyECC e;
    e.ciphertext = data;
    e.decrypt();
    return e.plaintext;
}