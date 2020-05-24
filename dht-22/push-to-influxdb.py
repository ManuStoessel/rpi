#!/usr/bin/env python
import time
import sys
import board
import adafruit_dht
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

try:
    influx_bucket = sys.argv[1]
except IndexError:
    print('push-to-influxdb.py <bucketname>\nSet URL to InfluxDB, org name and token by using the environment variables described here:\nhttps://github.com/influxdata/influxdb-client-python#via-environment-properties')
    sys.exit(1)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D18)

try:
    # Print the values to the serial port
    temperature_c = dhtDevice.temperature
    #temperature_f = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity
    #print(
    #    "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
    #        temperature_f, temperature_c, humidity
    #    )
    #)

except RuntimeError as error:
    print(error.args[0])
    sys.exit(1)

try:
    client = influxdb_client.InfluxDBClient.from_env_properties()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    temp = influxdb_client.Point("dht-22").tag("rpi", "home", "dht-22").field("temperature", temperature_c)
    humid = influxdb_client.Point("dht-22").tag("rpi", "home", "dht-22").field("humidity", humidity)

    write_api.write(bucket=bucket, record=[temp, humid])

except InfluxDBClientError as error:
    print(error.args[0])
    sys.exit(2)
except InfluxDBServerError as server_error:
    print(error.args[0])
    sys.exit(3)

sys.exit(0)

