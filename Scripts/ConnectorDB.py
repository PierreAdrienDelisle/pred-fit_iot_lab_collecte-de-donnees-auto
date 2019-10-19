# -*- coding: utf-8 -*-

### ConnectorDB : Tools to connect to an Influx DB
from influxdb import InfluxDBClient




## TESTING
# API Doc : https://influxdb-python.readthedocs.io/en/latest/api-documentation.html
client = InfluxDBClient(host='localhost', port=8086)
#client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin',ssl=True, verify_ssl=True)
client.create_database('pyexample') 
a = client.get_list_database()
print(a)
client.switch_database('pyexample') #focus this DB

#Insert data
#Example : Duration time of a brushing teeth
data_example = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 127
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-29T8:04:00Z",
        "fields": {
            "duration": 132
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-30T8:02:00Z",
        "fields": {
            "duration": 129
        }
    }
]

client.write_points(data_example)

#Query data
results = client.query('SELECT "duration" FROM "pyexample"."autogen"."brushEvents" GROUP BY "user"')
print(results.raw)
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