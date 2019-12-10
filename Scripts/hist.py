#!/bin/bash
# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt


def tab_from_data(pathname, datatype):
    with open(pathname, 'r') as outfile:
        loaded_data = json.load(outfile)
        res = []
        for x in loaded_data:
            if x["type"] == datatype:
                res.append((int(x["node"][3:]), x["mean"]))
        res = sorted(res)
        return res


def separate_data(data):
    lvalue = []
    lnode = []
    for x in data:
        lnode.append(x[0])
        lvalue.append(x[1])
    return lnode, lvalue


def histogram(pathname, datatype):
    data = tab_from_data(pathname, datatype)
    lnode, lvalue = separate_data(data)
    if datatype == "pressure":
        plt.bar(lnode, height=lvalue, bottom=900)
    else:
        plt.bar(lnode, height=lvalue)
    plt.savefig("pathname/hist.png")
