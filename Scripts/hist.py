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
        plt.bar(lnode, height=lvalue, bottom=0)
        plt.axis(ymin=min(lvalue)-10, ymax=max(lvalue)+10)
    else:
        plt.bar(lnode, height=lvalue)
    plt.title(datatype + " captured on each node")
    plt.savefig("hist.png")


#histogram("/home/sonzero/Documents/Work/pred-fit_iot_lab_collecte-de-donnees-auto/Scripts/logDataCollector09-12-2019-17_45_30.txt", "pressure")
