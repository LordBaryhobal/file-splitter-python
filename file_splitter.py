#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random

def split(inpath, outpath, depth=3):
    files = []
    words = []
    
    with open(inpath, "rb") as in_file:
        padded = False
        while True:
            bytes_ = in_file.read(4)
            if len(bytes_) == 0:
                break
            
            elif len(bytes_) < 4:
                padded = True
                to_add = 4-(len(bytes_)%4)
                bytes_ += bytes([to_add]*to_add)
            
            word = bytes_[0] << 24
            word += bytes_[1] << 16
            word += bytes_[2] << 8
            word += bytes_[3]
            words.append(word)
        
        if not padded:
            words.append(0x04040404)
    
    files.append(words)
    
    for i in range(depth):
        tmp = []
        for arr in files:
            tmp += sep(arr)
        
        files = tmp
    
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    
    for i, arr in enumerate(files):
        with open(os.path.join(outpath, f"{i}.dat"), "wb") as out_file:
            for word in arr:
                out_file.write(word.to_bytes(4, "big"))

def sep(arr1):
    arr2 = random_arr(len(arr1))
    arr3 = xor(arr1, arr2)
    for i in range(1, len(arr1), 2):
        arr2[i], arr3[i-1] = arr3[i-1], arr2[i]
    
    return (arr2, arr3)

def random_arr(size):
    return [random.randint(0,0xffffffff-1) for i in range(size)]

def xor(arr1, arr2):
    arr3 = []
    for b1, b2 in zip(arr1, arr2):
        arr3.append(b1^b2)
    return arr3

"""
A

A ^ k = a / A ^ a = k / a ^ k = A
a ^ b ^ c ^ d = A
(a^b) ^ (c^d) = A
ab ^ cd = A
"""

"""A

A ^ r = a
a ^ r2 = a2
a2 ^ r = b = A ^ r2"""


if __name__ == "__main__":
    split("./test.txt", "./test_out")