#!/bin/bash
# -*- coding: utf-8 -*-
import os
import json
import sys
import subprocess
import argparse
from datetime import datetime

parser=argparse.ArgumentParser(
    description='''Enable to launch a data collector to write in a file all logs of m3 nodes''',
    epilog="""----""")
parser.add_argument('ratio', type=float, nargs='?',const=1, default=0.3, help='The ratio of node you will take on 1 site.For example if 100 m3 nodes are avalaible on Lille, you will put 0.3 and get 20 nodes on Lille')
parser.add_argument('site', type=str, nargs='?',const=1, default="lille", help='The site where you are running the experiment')
args=parser.parse_args()

print(" ****************** \n * Data Collector *\n ****************** \n")
site = args.site
ratio = args.ratio
scriptRepertory = "/senslab/users/delisle/pred-fit_iot_lab_collecte-de-donnees-auto/Scripts/"
print("Site: "+str(site)+", Ratio: "+str(ratio))
rGetAliveNodes = subprocess.check_output("iotlab-experiment info --site "+site+" --state Alive --archi m3:at86rf231 -l", shell=True)
res = json.loads(rGetAliveNodes)
nbAliveNodes = len(res["items"])
nbSubmit = int(nbAliveNodes*ratio)
print("Launching an experiment with : "+str(nbSubmit)+" nodes")

rSubmit = subprocess.check_output('iotlab-experiment submit -n cron-Submit-auto -d 1 -l '+str(nbSubmit)+',archi=m3:at86rf231+site="'+site+'"+mobile=0,'+scriptRepertory+'firmwares/firmware-5donnees-iotlab-m3', shell=True)
experimentId = str(json.loads(rSubmit)["id"])
rWait = subprocess.check_output('iotlab-experiment wait --id '+experimentId, shell=True)
check1 = datetime.now()
rSerialAggregator = subprocess.check_output("serial_aggregator -i "+experimentId, shell=True)
print("R serial_aggregator")
print(rSerialAggregator)
check2 = datetime.now() - check1
print("TIME Serial aggregator")
print(abs(check2))
rawData = str(rSerialAggregator)
#arrayData = [{"node":,"timestamp":,"type":,"values":}]
capturedData = []
dataLines = rawData.splitlines()
for line in dataLines:
    data = line.split(";")
    dictData = {"node":data[1],"timestamp":data[0],"type":data[2],"value":data[3],"x":0,"y":0,"z":0}
    capturedData.append(dictData)

rGetCoords = subprocess.check_output("iotlab experiment get -r -i "+experimentId, shell=True)
nodes = json.loads(rGetCoords.encode('utf-8'))["items"]
dictCoords = {}
for node in nodes :
    dictCoords[node["network_address"].replace("."+site+".iot-lab.info","")] = {"x":node["x"].encode("utf-8"),"y":node["y"].encode("utf-8"),"z":node["z"].encode("utf-8")}

for data in capturedData:
    data["x"],data["y"],data["z"] = dictCoords[data["node"]]["x"],dictCoords[data["node"]]["y"],dictCoords[data["node"]]["z"]

print("Writing in log file...")
now = datetime.now()
date_time = now.strftime("%d-%m-%Y-%H_%M_%S")

with open(scriptRepertory+"log/logDataCollector"+date_time+".txt", 'w') as outfile:
    json.dump(capturedData, outfile)
print("Done !")
