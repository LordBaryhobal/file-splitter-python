#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import numpy as np
import time

def random_arr(size):
    return np.random.randint(0, 0xffffffff, size, dtype="uint32")

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
        
        if not self.words is None:
            n = len(self.words)
            arr1 = random_arr(n)
            arr2 = self.words ^ arr1
            for i in range(1, n, 2):
                arr1[i], arr2[i-1] = arr2[i-1], arr1[i]
            
            self.children[0].words = arr1
            self.children[1].words = arr2
            self.words = None  # memory optimisation
    
    def get_leaves(self):
        leaves = []
        
        if len(self.children) == 0:
            leaves.append(self)
        
        else:
            for child in self.children:
                leaves += child.get_leaves()
        
        return leaves

def split(inpath, outpath, seed, n):
    files = []
    words = []
    tree = Node()
    
    with open(inpath, "rb") as in_file:
        bytes_ = in_file.read()
        to_add = 4-(len(bytes_)%4)
        
        if to_add == 0:
            to_add = 4
        
        bytes_ += bytes([to_add]*to_add)
        
        tree.words = np.frombuffer(bytes_, dtype=">u4").copy()
    
    tree.build(seed, n)
    
    print("Writing")
    
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    
    for i, node in enumerate(tree.get_leaves()):
        print(f"File {i}", end="\r")
        with open(os.path.join(outpath, f"{i}.dat"), "wb") as out_file:
            out_file.write(node.words.astype(">u4").tobytes())
    
    print("Finished")

if __name__ == "__main__":
    t1 = time.time()
    split("./meme.mp4", "./meme_tree", 2378956, 32)
    t2 = time.time()
    print(f"{t2-t1:.6f}s")