XOR_KEY = "PQRST";
INPUT="acagaffjjd"


def decrypt_string(s):
    xor_len=len(XOR_KEY)
    ans=""
    idx=-1
    for ch in INPUT:
        idx+=1
        idx%=xor_len
        ans+=chr(ord(ch)^ord(XOR_KEY[idx]))
    return ans

final_ans=decrypt_string(INPUT)
print(final_ans)