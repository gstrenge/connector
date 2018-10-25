"""
This program runs on the server side and subscribes to a specific topic in
order to receive information from a specific publisher (Raspberry Pi)

The devices' GAIN was chosen to be 1. Since this is a 16 bits device, the measured
voltage will depend on the programmable GAIN. The following table shows the possible
reading range per chosen GAIN. A GAIN of 1 goes from -4.096V to 4.096V.
- 2/3 = +/-6.144V
-   1 = +/-4.096V
-   2 = +/-2.048V
-   4 = +/-1.024V
-   8 = +/-0.512V
-  16 = +/-0.256V

This means that the maximum range of this 16 bits device is +/-32767.
Thus, to convert bits to V, we divide 4.096 by 32767,
which gives us 0.000125. In conclusion, to convert this readings to mV
we just need to multiply the output times 0.125, which is done in the server
side (mqtt-connector) to prevent time delays.
"""
import os
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import DataFrameClient

def write_to_db(payload, db_client):
	#Edits received CSV file from broker to add actual mV values
	#And writes them into InfluxDB
	print("Received Message")
	#create new file and write the received msg on it
	with open('received.csv', 'wb') as fd:
	    fd.write(payload)
	#Create dataframe
	df = pd.read_csv('received.csv')
	#Convert from bits to mV
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

def main():
	"""
	MQTT Client connector in charge of receiving the 10 Hz csv files,
	perform calculations and store them in the database
	"""
	#influxdb information for connection -- right now is local	
	db_host = 'influxdb'
	db_port = 8086
	db_username = 'root'
	db_password = 'root'
	database = 'testing'
	
	#info of the MQTT broker
	host = "35.237.36.219"
	port = 1883
	keepalive = 30
	client_id = None #client_id is randomly generated
	topic = "usa/quincy/1"

	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			# Callback for when the client receives a CONNACK response from the server.
			print("Connected with result code {}".format(rc))
			# Subscribes to topic with QoS 2
			client.subscribe(topic, 2)
		else:
			print("Error in connection")

	def on_message(client, userdata, msg):
		# The callback for when a PUBLISH message is received from the server.
		#Detects an arriving message (CSV) and writes it in the db
	    payload = msg.payload
	    try:
	        write_to_db(payload, db_client)
	    except: #This needs to be changed
		    print("Error")

	# connects to database and creates new database
	db_client = DataFrameClient(host=db_host, port=db_port, username=db_username, password=db_password, database=database)
	db_client.create_database('testing')

	#Establish conection with broker and start receiving messages
	# Params -> Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
	# We set clean_session to False, so in case connection is lost, it'll reconnect with same ID
	# For debug purposes (client_id is not defined) we'll set it to True
	client = mqtt.Client(client_id=client_id, clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host, port, keepalive)
	
	# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
	client.loop_forever()

if __name__ == '__main__':
	main()