import unittest, os, time
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import DataFrameClient

def test_write_to_db():
	from src.mqtt_connector.subscriber import connect_to_db, write_to_db
	
	#Connects to local InfluxDB
	db_client = connect_to_db(host='localhost', port=8086, username='root', 
		password='root', database='testing')
	#Creates local Database
	db_client.create_database('testing')
	#Create testing CSV file with one mock up line
	now = datetime.now()
	one_line = str.encode("adc,channel,time_stamp,value\n1,1,{},100".format(now))
	with open("testing.csv", "wb") as csvfile:
		csvfile.write(one_line)
	f = open("testing.csv")
	payload = f.read()
	write_to_db(payload=payload, db_client=db_client)

	written = db_client.query('SELECT * FROM "measurements"')
	dataframe = written['measurements']
	value = dataframe['mV'][0] 
	#Remove mockup CSV file
	os.remove("testing.csv")
	#Deletes mockup DB
	db_client.drop_database('testing')
	assert value == 100*0.125
	#BUG : dataframe.index.values[0] has more precision than np.datetime64(now)
	#assert dataframe.index.values[0] == np.datetime64(now)

def test_broker_connection():
	from src.mqtt_connector.subscriber import connect_to_broker, subscribe_to_topic
	host = "localhost"
	port = 1883
	client_id = "TESTING_CLIENT"
	topic = "testing/topic"
	keepalive = 30

	def on_connect(client, userdata, flags, rc):
		subscribe_to_topic(topic=topic, client=client)
	
	client, connection = connect_to_broker(client_id=client_id, host=host, port=port, on_connect=on_connect, on_message=None, keepalive=keepalive)

	assert connection == 0