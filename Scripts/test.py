#!/bin/bash
# -*- coding: utf-8 -*-
import os
import json
import sys
import subprocess
import argparse
from datetime import datetime, timezone
import ast
import matplotlib.pyplot as plt
import numpy as np

scriptRepertory = "./"

def tab_from_data():
    with open(scriptRepertory+"logDataCollector"+"09-12-2019-17_45_30"+".txt", 'r') as outfile:
        loaded_data = json.load(outfile)
        l = []
        for x in loaded_data:
            if x["type"] == "pressure":
                l.append((int(x["node"][3:]), x["mean"]))
        l = sorted(l)
        return l

def separate_data(L):
    Lvalue = []
    Lnode = []
    for x in L:
        Lnode.append(x[0])
        Lvalue.append(x[1])
    return Lnode, Lvalue

L = tab_from_data()
LNode, LValue = separate_data(L)

plt.bar(LNode, height=LValue)
plt.savefig("hist.png")
