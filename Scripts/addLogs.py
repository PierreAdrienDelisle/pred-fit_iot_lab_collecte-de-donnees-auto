# -*- coding: utf-8 -*-

### AddLogs : adding every file in a /log/ directory
import json
import argparse
import subprocess
import os

print("Adding logs...")
directory = "./log/"
for file in os.listdir(directory):
    print(file)
    subprocess.check_output("python.exe ./ConnectorDB.py -i "+directory+file,shell=True)

print("Done")
