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
#rSerialAggregator = subprocess.check_output("serial_aggregator -i "+experimentId, shell=True)

rGetCoords = subprocess.check_output("iotlab experiment get -r -i "+experimentId, shell=True)
nodes = json.loads(rGetCoords)["items"]
dictCoords = {}
for node in nodes :
    dictCoords[node["network_address"]] = [node["x"],node["y"],node["z"]]
print(dictCoords)

#rStop = subprocess.check_output('iotlab-experiment stop --id '+experimentId, shell=True)
