# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:24:32 2022

@author: 86137
"""

import random
from  math import ceil
import time

IV=" 7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e"
IV = int(IV, 16)
a = []
for i in range(0, 8):
    a.append(0)
    a[i] = (IV >> ((7 - i) * 32)) & 0xFFFFFFFF
IV = a

def rotate_left(x, n):  #循环移位
    n = n%32
    left = (x << n) % (2 ** 32)
    right = (x >> (32 - n)) % (2 ** 32)
    return left ^ right


T_j = []                       #常量值
for i in range(0, 16):
    T_j.append(0)
    T_j[i] = 0x79cc4519  
for i in range(16, 64):
    T_j.append(0)
    T_j[i] = 0x7a879d8a

def out_hex(list1):
    for i in list1:
        print("%08x" % i)
    print("\n")


def str2byte(msg): # 字符串转换成byte数组
    ml = len(msg)
    msg_byte = []
    msg_bytearray = msg.encode('utf-8')
    for i in range(ml):
        msg_byte.append(msg_bytearray[i])
    return msg_byte

def byte2str(msg): # byte数组转换成字符串
    ml = len(msg)
    str1 = b""
    for i in range(ml):
        str1 += b'%c' % msg[i]
    return str1.decode('utf-8')

def hex2byte(msg): # 16进制字符串转换成byte数组
    ml = len(msg)
    if ml % 2 != 0:
        msg = '0'+ msg
    ml = int(len(msg)/2)
    msg_byte = []
    for i in range(ml):
        msg_byte.append(int(msg[i*2:i*2+2],16))
    return msg_byte

def byte2hex(msg): # byte数组转换成16进制字符串
    ml = len(msg)
    hexstr = ""
    for i in range(ml):
        hexstr = hexstr + ('%02x'% msg[i])
    return hexstr


def decimalToHex(decValue):    #将十进制转换为十六进制
    hex=""
    while decValue !=0:
        hexValue=decValue%16   
        hex=toHexChar(hexValue)+hex
        decValue=decValue//16  
    return hex


def toHexChar(hexValue):     #十六进制转换成字符串
    if 0<=hexValue<=9:
        return chr(hexValue+ord('0'))
    else:
        return chr(hexValue-10+ord('A'))


def FF(X, Y, Z, j):     #布尔函数
        FF_j = 0
        if j < 16:
            FF_j = X^Y^Z
        elif j >= 16:
            FF_j = (X&Y) | (X&Z) | (Y&Z)
        return FF_j

def GG(X, Y, Z, j):
        GG_j = 0
        if j < 16:
            GG_j = X^Y^Z
        elif j >= 16:
            GG_j = (X&Y) | (~X&Z)
        return GG_j


def P_0(X):       #置换函数
    return X ^ (rotate_left(X, 9)) ^ (rotate_left(X, 17))

def P_1(X):
    return X ^ (rotate_left(X, 15)) ^ (rotate_left(X, 23))

def CF(V_i, B_i):        #压缩函数,输入分别为256bit的中间值和512bit的待压缩数据
    W = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + B_i[k]*weight
            weight = int(weight/0x100)
        W.append(data)

    for j in range(16, 68):
        W.append(0)
        W[j] = P_1(W[j-16] ^ W[j-9] ^ (rotate_left(W[j-3], 15))) ^ (rotate_left(W[j-13], 7)) ^ W[j-6]
        str1 = "%08x" % W[j]
    W_1 = []
    for j in range(0, 64):
        W_1.append(0)
        W_1[j] = W[j] ^ W[j+4]
        str1 = "%08x" % W_1[j]

    A, B, C, D, E, F, G, H = V_i

    for j in range(0, 64):
        SS1 = rotate_left(((rotate_left(A, 12)) + E + (rotate_left(T_j[j], j))) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ (rotate_left(A, 12))
        TT1 = (FF(A, B, C, j) + D + SS2 + W_1[j]) & 0xFFFFFFFF
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
        D = C
        C = rotate_left(B, 9)
        B = A
        A = TT1
        H = G
        G = rotate_left(F, 19)
        F = E
        E = P_0(TT2)

        A = A & 0xFFFFFFFF
        B = B & 0xFFFFFFFF
        C = C & 0xFFFFFFFF
        D = D & 0xFFFFFFFF
        E = E & 0xFFFFFFFF
        F = F & 0xFFFFFFFF
        G = G & 0xFFFFFFFF
        H = H & 0xFFFFFFFF

    V_i_1 = []
    V_i_1.append(A ^ V_i[0])
    V_i_1.append(B ^ V_i[1])
    V_i_1.append(C ^ V_i[2])
    V_i_1.append(D ^ V_i[3])
    V_i_1.append(E ^ V_i[4])
    V_i_1.append(F ^ V_i[5])
    V_i_1.append(G ^ V_i[6])
    V_i_1.append(H ^ V_i[7])
    return V_i_1

def hash_msg(msg):
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])


    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])

    V = []
    V.append(IV)
    for i in range(0, group_count):
        V.append(CF(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result


def Hash_reduced_SM3(msg,Hexstr = 0):
    if(Hexstr):
        msg_byte = hex2byte(msg)
    else:
        msg_byte = str2byte(msg)
    return hash_msg(msg_byte)

        
def Rho_method(n):
    x0=decimalToHex(random.randint(0,2**512))
    x1=x0
    x2=x0
    for i in range(2**n):
        x1=Hash_reduced_SM3(x1)
        x2=Hash_reduced_SM3(Hash_reduced_SM3(x2))
        n_hex=n//8
        if(x1[:n_hex]==x2[:n_hex]):
          x2=x1
          x1=x0
          for j in range(i):
              if(Hash_reduced_SM3(x1)[:n_hex]==Hash_reduced_SM3(x2)[:n_hex]):
                  print("成功找到一对碰撞")
                  print(x1,x2)
                  return 0
              else:
                  x1=Hash_reduced_SM3(x1)
                  x2=Hash_reduced_SM3(x2)
        else:
             print("不是一对碰撞")   
             
             
if __name__ == '__main__':
    n=int(input("碰撞位数为："))
    Rho_method(n)