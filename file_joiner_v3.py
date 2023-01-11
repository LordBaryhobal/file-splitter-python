#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
import time
import random

class DecodingError(Exception):
    pass

class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.words = None
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def build(self, seed, n):
        random.seed(seed)
        
        self.children = []
        leaves = [self]
        for i in range(1, n):
            j = random.randint(0, i-1)
            node = leaves.pop(j)
            node.split()
            leaves += node.children
        
        random.seed(time.time())
    
    def split(self):
        self.add_child(Node())
        self.add_child(Node())
    
    def join(self):
        if len(self.children):
            for child in self.children:
                child.join()
            
            a, b = self.children
            
            for j in range(1, len(a.words), 2):
                a.words[j], b.words[j-1] = b.words[j-1], a.words[j]
            
            self.words = a.words ^ b.words
    
    def get_leaves(self):
        leaves = []
        
        if len(self.children) == 0:
            leaves.append(self)
        
        else:
            for child in self.children:
                leaves += child.get_leaves()
        
        return leaves

def join(inpath, outpath, seed, n):
    paths = sorted(os.listdir(inpath), key=lambda p: int(p.split(".")[0]))
    if len(paths) != n:
        raise DecodingError("Incorrect number of files")
    
    files = []
    
    tree = Node()
    tree.build(seed, n)
    leaves = tree.get_leaves()
    
    print("Reading")
    for node, f in zip(leaves, paths):
        #words = []
        with open(os.path.join(inpath, f), "rb") as in_file:
            node.words = np.frombuffer(in_file.read(), dtype=">u4").copy()
    
    print("Joining")
    tree.join()
    
    result = tree.words
    
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
    join("./meme_tree", "./joined_tree.mp4", 2378956, 32)
    t2 = time.time()
    print(f"{t2-t1:.6f}s")