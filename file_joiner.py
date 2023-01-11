#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def join(inpath, outpath):
    result = None
    
    paths = sorted(os.listdir(inpath))
    files = []
    
    for f in paths:
        words = []
        with open(os.path.join(inpath, f), "rb") as in_file:
            while True:
                bytes_ = in_file.read(4)
                if len(bytes_) == 0:
                    break
                
                word = bytes_[0] << 24
                word += bytes_[1] << 16
                word += bytes_[2] << 8
                word += bytes_[3]
                words.append(word)
        
        files.append(words)
        """if result is None:
            result = words
        
        else:
            result = xor(result, words)"""
    
    while len(files) > 1:
        tmp = []
        for i in range(0, len(files), 2):
            a, b = files[i:i+2]
            for j in range(1, len(a), 2):
                a[j], b[j-1] = b[j-1], a[j]
            
            tmp.append(xor(a, b))
        
        files = tmp
    
    result = files[0]
    
    to_unpad = 0
    if result[-1] == 0x04040404:
        result.pop(-1)
    
    else:
        to_unpad = (result[-1] & 0xff)
    
    with open(outpath, "wb") as out_file:
        if to_unpad:
            last = result[-1]
            result = result[:-1]
        
        for word in result:
            out_file.write(word.to_bytes(4, "big"))
        
        if to_unpad:
            bytes_ = last.to_bytes(4, "big")[:-to_unpad]
            out_file.write(bytes_)

def xor(arr1, arr2):
    arr3 = []
    for b1, b2 in zip(arr1, arr2):
        arr3.append(b1^b2)
    return arr3

if __name__ == "__main__":
    join("./test_out", "./joined.txt")