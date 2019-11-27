# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 15:22:33 2019

@author: Pierre-adrien
"""

import os
import json

import subprocess
print(" ****************** \n * Data Collector *\n ****************** \n")
rGetAliveNodes = subprocess.check_output("iotlab-experiment info --site lille --state Alive --archi m3:at86rf231 -l", shell=True)
res = json.loads(rGetAliveNodes)
nbAliveNodes = len(res["items"])
nbSubmit = nbAliveNodes*2//3
print("Launching an experiment with : "+str(nbSubmit)+" nodes")

rSubmit = subprocess.check_output('iotlab-experiment submit -n SSH-python-Submit -d 1 -l '+str(5)+',archi=m3:at86rf231+site=lille+mobile=0,./firmwares/firmware-pressure-light1.iotlab-m3', shell=True)
experimentId = str(json.loads(rSubmit)["id"])
rWait = subprocess.check_output('iotlab-experiment wait --id '+experimentId, shell=True)

rSerialAggregator = subprocess.check_output("serial_aggregator -i "+experimentId, shell=True)
rawData = str(rSerialAggregator)
#arrayData = [{"node":,"timestamp":,"type":,"values":}]
capturedData = []
dataLines = rawData.splitlines()
for line in dataLines:
    data = line.split(";")
    dictData = {"node":data[1],"timestamp":data[0],"value":data[2],"x":0,"y":0,"z":0}
    capturedData.append(dictData)

print("Captured Data")
print(capturedData)


rGetCoords = subprocess.check_output("iotlab experiment get -r -i "+experimentId, shell=True)
nodes = json.loads(rGetCoords.encode('utf-8'))["items"]
dictCoords = {}
for node in nodes :
    dictCoords[node["network_address"].replace(".lille.iot-lab.info","")] = {"x":node["x"].encode("utf-8"),"y":node["y"].encode("utf-8"),"z":node["z"].encode("utf-8")}

print("dictCoords")
print(dictCoords)

for data in capturedData:
    data["x"],data["y"],data["z"] = dictCoords[data["node"]]["x"],dictCoords[data["node"]]["y"],dictCoords[data["node"]]["z"]

print("Final Capture : ")
print(capturedData)

#rStop = subprocess.check_output('iotlab-experiment stop --id '+experimentId, shell=True)
