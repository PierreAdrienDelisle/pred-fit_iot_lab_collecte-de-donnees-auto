#!/bin/bash
# -*- coding: utf-8 -*-
import os
import json
import sys
import subprocess
import argparse
from datetime import datetime, timezone
import ast
import time
import re
import pty


## Enable to have options and a --help
parser=argparse.ArgumentParser(
    description='''Enable to launch a data collector to write in a file all logs of m3 nodes''',
    epilog="""----""")
parser.add_argument('ratio', type=int, nargs='?',const=1, default=30, help='The ratio of node you will take on 1 site.For example if 200 M3 nodes are avalaible on Lille, you will put 30 and get 60 nodes on Lille')
parser.add_argument('site', type=str, nargs='?',const=1, default="lille", help='The site where you are running the experiment')
args=parser.parse_args()

## Beginning of the script
print(" ****************** \n * Data Collector *\n ****************** \n")
site = args.site
ratio = args.ratio
repo = "/senslab/users/delisle/pred-fit_iot_lab_collecte-de-donnees-auto/Scripts/"
print("Site: "+str(site)+", Ratio: "+str(ratio)+"%")

## Open a ghost terminal to make serial_aggregator working (need for raw_input func)
master, slave = pty.openpty()
s_name = os.ttyname(slave)
print(s_name)


## Look after the number of avalaible nodes and lauch an experiment with the ratio
rGetAliveNodes = subprocess.check_output("iotlab-experiment info --site "+site+" --state Alive --archi m3:at86rf231 -l", shell=True)
res = json.loads(rGetAliveNodes.decode('utf-8'))
nbAliveNodes = len(res["items"])
nbSubmit = int(nbAliveNodes*ratio/100)
if(nbSubmit < 10):
    print("Too few nodes avalaible")
    print("Only "+nbSubmit+" nodes")
else:
    print("Launching an experiment with : "+str(nbSubmit)+" nodes")
    rSubmit = subprocess.check_output('iotlab-experiment submit -n AutoCollect -d 1 -l '+str(nbSubmit)+',archi=m3:at86rf231+site="'+site+'"+mobile=0,'+repo+'firmwares/firmware-5donnees-iotlab-m3,TestMonitor', shell=True)
    experimentId = str(json.loads(rSubmit.decode('utf-8'))["id"])

    ## Wait for the experiment to run and launch serial_aggregator
    wait1 = datetime.now()
    rWait = subprocess.check_output('iotlab-experiment wait --id '+experimentId, shell=True)
    wait2 = datetime.now() - wait1
    print("Time waited")
    print(abs(wait2))
    print(json.loads(rWait.decode('utf-8')))

    check1 = datetime.now()
    rSerialAggregator = subprocess.check_output("serial_aggregator -i "+experimentId+" < "+s_name, shell=True)
    rSerialAggregator = json.loads(json.dumps(rSerialAggregator.decode('utf-8')))
    check2 = datetime.now() - check1
    print("Time Serial aggregator")
    print(abs(check2))
    rawData = str(rSerialAggregator)

    ## Split up data from serial_aggregator and put it in a JSON format
    capturedData = []
    dataLines = rawData.splitlines()
    for line in dataLines:
        data = line.split(";")
        dictData = {"node":data[1],"timestamp":float(data[0]),"type":data[2],"value":data[3],"mean":0}
        capturedData.append(dictData)

    for elem in capturedData:
        sum = 0
        n = 0
        elem["timestamp"] = datetime.fromtimestamp(elem["timestamp"], timezone.utc).strftime("%d/%m/%Y-%H:%M:%S.%f")
        elem["value"] = ast.literal_eval(elem["value"])
        for v in elem["value"]:
            sum += v
            n += 1
        elem["mean"] = sum/n

    ## Radio output
    print("Radio output")
    directory = "/senslab/users/delisle/.iot-lab/"+experimentId+"/radio/"
    time.sleep(5) #Wait for radio output to be ready
    regex = re.compile(r"[0-9]+[.][0-9]+[\s][0-9]+[\s][0-9]+[\s][0-9]+[\s][0-9]+[\s][0-9]+[\s][-+\s][0-9]+") #Regex to find radio output lines
    rssiOutput = []
    for file in os.listdir(directory):
        node = file.split(".")[0].split("_")
        node = node[0]+'-'+node[1]
        with open(directory+file,'r') as f:
            for line in f:
                if(re.match(regex, line)):
                    rssiTab = line.split()
                    rssiVal = rssiTab[6]
                    rssiTimestamp = datetime.fromtimestamp(float(rssiTab[3]+rssiTab[4]), timezone.utc).strftime("%d/%m/%Y-%H:%M:%S.%f")
                    rssiChannel = rssiTab[5]
                    rssiOutput.append({"node":node,"value":rssiVal,"time":rssiTimestamp,"channel":rssiChannel})
    dataDict = {"capturedData":capturedData,"rssi":rssiOutput}
    ## Write in a log file the captured data
    print("Writing in log file...")
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y-%H_%M_%S")
    filename = repo+"log/logDataCollector"+date_time+".json"
    with open(filename, 'w') as outfile:
         json.dump(dataDict, outfile)
    print("Done !")
