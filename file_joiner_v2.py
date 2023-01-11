#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
import time

def join(inpath, outpath):
    paths = sorted(os.listdir(inpath), key=lambda p: int(p.split(".")[0]))
    files = []
    
    print("Reading")
    for f in paths:
        #words = []
        with open(os.path.join(inpath, f), "rb") as in_file:
            words = np.frombuffer(in_file.read(), dtype=">u4").copy()
            files.append(words)
    
    print("Joining")
    I = 0
    while len(files) > 1:
        tmp = []
        print(f"Step {I}")
        I += 1
        for i in range(0, len(files), 2):
            a, b = files[i:i+2]
            for j in range(1, len(a), 2):
                a[j], b[j-1] = b[j-1], a[j]
            
            tmp.append(a ^ b)
        
        files = tmp
    
    result = files[0]
    
    to_unpad = 0
    if result[-1] == 0x04040404:
        result = result[:-1]
    
    else:
        to_unpad = (result[-1] & 0xff)
    
    print("Writing")
    with open(outpath, "wb") as out_file:
        if to_unpad:
            last = result[-1]
            result = result[:-1]
        
        out_file.write(result.astype(">u4").tobytes())
        
        if to_unpad:
            bytes_ = int(last).to_bytes(4, "big")[:-to_unpad]
            out_file.write(bytes_)
    
    print("Finished")
if __name__ == "__main__":
    t1 = time.time()
    join("./meme", "./joined.mp4")
    t2 = time.time()
    print(f"{t2-t1:.6f}s")