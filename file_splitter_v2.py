#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import numpy as np
import time

def split(inpath, outpath, depth=3):
    files = []
    words = []
    
    with open(inpath, "rb") as in_file:
        #padded = False
        bytes_ = in_file.read()
        to_add = 4-(len(bytes_)%4)
        
        if to_add == 0:
            to_add = 4
        
        bytes_ += bytes([to_add]*to_add)
        
        words = np.frombuffer(bytes_, dtype=">u4").copy()
        files.append(words)
        
        """while True:
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
            words.append(0x04040404)"""
    
    #files.append(np.array(words, dtype="uint32"))
    
    for i in range(depth):
        print(f"round {i}")
        tmp = []
        for j, arr in enumerate(files):
            print(f"{j/(2**i)*100:.2f}%", end="\r")
            tmp += sep(arr)
        
        files = tmp
    
    print("Writing")
    
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    
    for i, arr in enumerate(files):
        print(f"File {i}", end="\r")
        with open(os.path.join(outpath, f"{i}.dat"), "wb") as out_file:
            out_file.write(arr.astype(">u4").tobytes())
    
    print("Finished")

def sep(arr1):
    arr2 = random_arr(len(arr1))
    arr3 = arr1 ^ arr2
    for i in range(1, len(arr1), 2):
        arr2[i], arr3[i-1] = arr3[i-1], arr2[i]
    
    return (arr2, arr3)

def random_arr(size):
    #return [random.randint(0,0xffffffff-1) for i in range(size)]
    return np.random.randint(0, 0xffffffff, size, dtype="uint32")

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
    t1 = time.time()
    split("./meme.mp4", "./meme", 5)
    t2 = time.time()
    print(f"{t2-t1:.6f}s")