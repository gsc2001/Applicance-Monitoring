import sys

XOR_KEY = "PQRST";
INPUT=input()
print(len(INPUT))
RAND_MASTER=12
RAND_NUM=0
print("Input is ",INPUT)
def decrypt_string(s):
    xor_len=len(XOR_KEY)
    ans=""
    global RAND_NUM
    idx=-1
    for ch in INPUT:
        # print(ch)
        idx+=1
        RAND_NUM+=1
        idx%=xor_len
        # print(ord(XOR_KEY[idx]))
        # print(ord(ch))
        num=ord(ch)^ord(XOR_KEY[idx])
        print(num)
        num-=RAND_NUM
        left=num
        if left<0:
            num=256-abs(left)
        ans+=chr(num)
        # print("******")
    return ans

final_ans=decrypt_string(INPUT)
print(final_ans)