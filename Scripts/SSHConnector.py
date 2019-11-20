# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 15:22:33 2019

@author: Pierre-adrien
"""

from fabric import Connection

c = Connection(host="lille.iot-lab.info",user="delisle",connect_kwargs={"key_filename": "./test.ppk",}, )
result = c.run('iotlab-experiment submit -n SSH-python-test -d 15 -l 1,archi=m3:at86rf231+site=lille+mobile=0')



