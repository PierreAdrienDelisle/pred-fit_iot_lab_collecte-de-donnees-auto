# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 15:22:33 2019

@author: Pierre-adrien
"""

from fabric import Connection
import json

keyF = "openssh.key"
'''
with open(keyF) as t:
    for l in t:
        print(l)
'''

c = Connection(host="lille.iot-lab.info",user="delisle",connect_kwargs={"key_filename": keyF,}, )

rGetAliveNodes = c.run("iotlab-experiment info --site lille --state Alive --archi m3:at86rf231 -l")
res = json.loads(rGetAliveNodes.stdout)
nbAliveNodes = len(res["items"])
nbSubmit = nbAliveNodes*2//3

rSubmit = c.run('iotlab-experiment submit -n SSH-python-Submit -d 10 -l '+str(nbSubmit)+',archi=m3:at86rf231+site=lille+mobile=0')
experimentId = str(json.loads(rSubmit.stdout)["id"])
rWait = c.run('iotlab-experiment wait --id '+experimentId)
rLS = c.run('ls')

rGetCoords = c.run("iotlab experiment get -r -i "+experimentId)
nodes = json.loads(rGetCoords.stdout)["items"]
dictCoords = {}
for node in nodes :
    dictCoords[node["network_address"]] = [node["x"],node["y"],node["z"]]


    
"""
rGetNodes = c.run("iotlab-experiment get -p --id "+experimentId)
nodes = json.loads(rGetNodes.stdout)["nodes"]
"""
#rSerialAggregator = c.run("serial_aggregator -i "+experimentId)

#result3 = c.run("iotlab-experiment submit -n SSH-python-test-firmware -d 15 -l 1,archi=m3:at86rf231+site=lille+mobile=0,tutorial_m3.elf")



