import os
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import DataFrameClient

def connect_to_db(host, port, username, password, database):
	#creating an influxdb client instance
	db_client = DataFrameClient(host=host, port=port, username=username, password=password, database=database)
	return db_client
	
def connect_to_broker(client_id, host, port, keepalive, on_connect, on_message):
	# Params -> Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
	# We set clean_session False, so in case connection is lost, it'll reconnect with same ID
	client = mqtt.Client(client_id=client_id, clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	connection = client.connect(host, port, keepalive)
	return (client, connection)

def write_to_db(payload, db_client):
	#Edits received CSV file from broker to add actual mV values
	#And writes them into InfluxDB
	print("Received Message")
	#create new file and write the received msg on it
	with open('received.csv', 'wb') as fd:
	    fd.write(payload)
	#Create dataframe
	df = pd.read_csv('received.csv')
	#Calculate actual mV measurement
	df['mV'] = df['value']*0.125
	#Delete old value of bits
	del df['value']
	#Convert the received timestamp into a pandas datetime object
	df['date_time'] = pd.to_datetime(df['time_stamp'])
	#set a DateTime index and delete the old time_stamp columns
	df = df.set_index(pd.DatetimeIndex(df['date_time']))
	del df['time_stamp'], df['date_time']
	#Seperate the dataframe by groups of adc's and channels
	#Given we are only going to be using one field ('mV')
	#Tags are given as a dict
	grouped = df.groupby(['adc','channel'])
	for group in grouped.groups:
		adc, channel = group
		tags = dict(adc=adc, channel=channel)
		sub_df = grouped.get_group(group)[['mV']]
		db_client.write_points(sub_df, 'measurements', tags=tags)
	print('Data Written to DB')
	os.remove('received.csv')

def subscribe_to_topic(topic, client):
	client.subscribe(topic, 2)

def main():
	"""
	MQTT Client connector in charge of receiving the 10 Hz csv files,
	perform calculations and store them in the database
	"""
	#influxdb information for connection -- right now is local	
	db_host = 'localhost'
	db_port = 8086
	db_username = 'root'
	db_password = 'root'
	database = 'testing'
	
	#info of the MQTT broker
	host = "35.237.36.219"
	port = 1883
	keepalive = 30
	client_id = "RECEIVER_TEST"
	topic = "usa/quincy/1"

	db_client = connect_to_db(host=db_host, port=db_port, username=db_username, password=db_password, database=database)

	def on_connect(client, userdata, flags, rc):
		# The callback for when the client receives a CONNACK response from the server.
		# Subscribing in on_connect() means that if we lose the connection and reconnect then 
		# subscriptions will be renewed.
		print("Connected with result code {}".format(rc))
		subscribe_to_topic(topic=topic, client=client)

	def on_message(client, userdata, msg):
		# The callback for when a PUBLISH message is received from the server.
		#Detects an arriving message (CSV) and writes it in the db
	    payload = msg.payload
	    write_to_db(payload, db_client)

	#Establish conection with broker and start receiving messages
	client, connection = connect_to_broker(client_id=client_id, host=host, port=port, keepalive=keepalive, on_connect=on_connect, on_message=on_message)
	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	client.loop_forever()

if __name__ == '__main__':
	main()