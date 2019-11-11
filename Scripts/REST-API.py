# -*- coding: utf-8 -*-

### REST-API : Tools to communicate in REST
import requests
from requests.auth import HTTPBasicAuth
import json

myAuth = HTTPBasicAuth('user', 'pass')

apiServer = "https://www.iot-lab.info/api"

rGetTotal = requests.get(apiServer+"/experiments/total", auth=myAuth)
res = json.loads((rGetTotal.text))


    
submitData = {"experiment": json.dumps({"type":"alias",
             "duration":20,
             "name":"ApiRestPython",
             "nodes":[{"alias":1,"nbnodes":3,"properties":{"archi":"m3:at86rf231","site":"lille","mobile":"false"}}],
             "firmwareassociations":[{"nodes":[1],"firmwarename":"iotlab_m3_tutorial"}],
             "profileassociations":None,
             })
            }
rSubmit = requests.post(apiServer+"/experiments",files=submitData, auth=myAuth)

resSubmit = rSubmit.text
print(resSubmit)
exp_id = json.loads((rSubmit.text))["id"]

#experiment.json: {"type":"alias","duration":20,"name":"","nodes":[{"alias":1,"nbnodes":3,"properties":{"archi":"m3:at86rf231","site":"lille","mobile":false}}],"firmwareassociations":null,"profileassociations":null}

