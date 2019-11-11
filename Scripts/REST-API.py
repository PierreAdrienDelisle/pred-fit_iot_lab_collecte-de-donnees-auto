# -*- coding: utf-8 -*-

### REST-API : Tools to communicate in REST
import requests
from requests.auth import HTTPBasicAuth
import json

myAuth = HTTPBasicAuth('user', 'pass')

apiServer = "https://www.iot-lab.info/api"

rGetTotal = requests.get(apiServer+"/experiments/total", auth=myAuth)
res = json.loads((rGetTotal.text))



headers = {"content-type":"multipart/form-data"}
submitData =  json.dumps({"experiment":
                {"type":"alias",
                 "duration":2,
                 "name":"ApiRestPython",
                 "nodes":[{"alias":1,"nbnodes":3,"properties":{"archi":"m3:at86rf231","site":"lille","mobile":"false"}}],
                 "firmwareassociations":None,
                 "profileassociations":None,
                 }
                })
rSubmit = requests.post(apiServer+"/experiments/",data=submitData, auth=myAuth,headers=headers)

resSubmit = rSubmit.text
print(resSubmit)

#experiment.json: {"type":"alias","duration":20,"name":"","nodes":[{"alias":1,"nbnodes":3,"properties":{"archi":"m3:at86rf231","site":"lille","mobile":false}}],"firmwareassociations":null,"profileassociations":null}