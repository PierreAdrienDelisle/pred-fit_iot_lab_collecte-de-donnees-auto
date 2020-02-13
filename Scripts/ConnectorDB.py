# -*- coding: utf-8 -*-

### ConnectorDB : Tools to connect to an Influx DB
from influxdb import InfluxDBClient
import json
import argparse

## Enable to have options and a --help
parser=argparse.ArgumentParser(
    description='''Connect to an influxDB database, the expected format is like DataCollector : {rssi: ..., capturedData: ... }''',
    epilog="""----""")
parser.add_argument('-i', '--input', help='Input file name', required=True)
parser.add_argument('host', type=str, nargs='?',const=1, default="localhost", help='The ip adress of the DB, by default localhost')
parser.add_argument('port', type=int, nargs='?',const=1, default="8086", help='The port of the DB, by default 8086')
parser.add_argument('database', type=str, nargs='?',const=1, default="dbTest", help='The name of the database')

args=parser.parse_args()
file = args.input
host = args.host
port = args.port
database = args.database

# API Doc : https://influxdb-python.readthedocs.io/en/latest/api-documentation.html
client = InfluxDBClient(host=host, port=port)
client.switch_database(database) #focus this DB

#Insert data
data_example = []
for line in open(file, 'r'):
    data_example.append(json.loads(line))

#Get capturedData that contains : light, pressure measurements
capturedData = data_example[0]["capturedData"]
dataInfluxCaptured = []
for elem in capturedData:
    dataInfluxCaptured.append({"measurement":elem["type"],
                 "time":elem["timestamp"],
                 "tags":{"node":elem["node"]},
                 "fields": {"mean": elem["mean"],
                         }
                     })
client.write_points(dataInfluxCaptured) #push into DB


#Get rssiData that contains : rssi measurements
rssiData = data_example[0]["rssi"]
dataInfluxRssi = []
for elem in rssiData:
    if(elem != {}):
        dataInfluxRssi.append({"measurement":"rssi",
                 "time":elem["time"],
                 "tags":{"node":elem["node"]},
                 "fields": {"value": elem["value"],
                            "channel":elem["channel"],
                         }

            })
client.write_points(dataInfluxRssi)

#Query data
#results = client.query('SELECT "value" FROM "rssi"')
#print(results.raw)
