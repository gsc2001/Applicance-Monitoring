import sys

XOR_KEY = "AB12:>";
INPUT=input()
# with open("ans.txt",'r') as fd:
#     INPUT=fd.read()


print("Input received is ", INPUT)
print(len(INPUT))
RAND_MASTER=12
RAND_NUM=0

##############################
ascii_to_char=dict()
char_to_ascii=dict()


def populate_stuff():
    for i in range(64):
        ch=chr(i+44)
        char_to_ascii[ch]=i
        ascii_to_char[i]=ch
populate_stuff()

#######################################
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
        RAND_NUM%=RAND_MASTER
        idx%=xor_len
        # print(ord(XOR_KEY[idx]))
        # print(ord(ch))
        num=char_to_ascii[ch]^char_to_ascii[XOR_KEY[idx]]
        print(num)
        num-=RAND_NUM
        left=num
        if left<0:
            num=64-abs(left)
        ans+=ascii_to_char[num]
        # print("******")
    return ans

final_ans=decrypt_string(INPUT)
print(final_ans)