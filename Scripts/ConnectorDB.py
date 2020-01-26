# -*- coding: utf-8 -*-

### ConnectorDB : Tools to connect to an Influx DB
from influxdb import InfluxDBClient
import json
import argparse

parser=argparse.ArgumentParser(
    description='''Connect to an influxDB database, the expected format is like DataCollector : {rssi,capturedData}''',
    epilog="""----""")
parser.add_argument('-i', '--input', help='Input file name', required=True)
parser.add_argument('host', type=str, nargs='?',const=1, default="localhost", help='The ip adress of the DB, by default localhost')
parser.add_argument('port', type=int, nargs='?',const=1, default="8086", help='The port of the DB, by default 8086')

args=parser.parse_args()
file = args.file
host = args.host
port = args.port
## TESTING
# API Doc : https://influxdb-python.readthedocs.io/en/latest/api-documentation.html
client = InfluxDBClient(host=host, port=port)
#client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin',ssl=True, verify_ssl=True)
client.create_database('dbTest')
a = client.get_list_database()
client.switch_database('dbTest') #focus this DB

#Insert data
#Example : Duration time of a brushing teeth
data_example = []
for line in open(file, 'r'):
    data_example.append(json.loads(line))

capturedData = data_example[0]["capturedData"]
dataInfluxCaptured = []
for elem in capturedData:
    dataInfluxCaptured.append({"measurement":elem["type"],
                 "time":elem["timestamp"],
                 "tags":{"node":elem["node"]},
                 "fields": {"mean": elem["mean"],
                         }
                     })

client.write_points(dataInfluxCaptured)

rssiData = data_example[0]["rssi"]
dataInfluxRssi = []
for elem in rssiData:
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
'''
points = results.get_points(tags={'user': 'Carol'})
for point in points: #☻Iterate over each point to show duration
    print("Time: %s, Duration: %i" % (point['time'], point['duration']))



results2 = client.query('SELECT "duration" FROM "pyexample"."autogen"."brushEvents" GROUP BY "brushId"')
points2 = results2.get_points(tags={'brushId': '6c89f539-71c6-490d-a28d-6c5d84c0ee2f'})
brush_usage_total = 0
for point in points2: # Iterate and use it to see global measurements
    brush_usage_total = brush_usage_total + point['duration']
if brush_usage_total > 350:
    print("You've used your brush head for %s seconds, more than the recommended amount! Time to replace your brush head!" % brush_usage_total)
'''
