"""
This program runs on the server side and subscribes to a specific topic in
order to receive information from a specific publisher (Raspberry Pi)

The devices' GAIN was chosen to be 1. Since this is a 16 bits device, the measured
voltage will depend on the programmable GAIN. The following table shows the possible
reading range per chosen GAIN. A GAIN of 1 goes from -4.096V to 4.096V.
- 2/3 = +/-6.144V
-	1 = +/-4.096V
-	2 = +/-2.048V
-	4 = +/-1.024V
-	8 = +/-0.512V
-  16 = +/-0.256V

This means that the maximum range of this 16 bits device is +/-32767.
Thus, to convert bits to V, we divide 4.096 by 32767,
which gives us 0.000125. In conclusion, to convert this readings to mV
we just need to multiply the output times 0.125, which is done in the server
side (mqtt-connector) to prevent time delays.
"""
import os, time
import json
import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import DataFrameClient

def wait_for_influxdb(db_client):
	"""Function to wait for the influxdb service to be available"""
	try:
		db_client.ping()
		print("connected to db")
		return None
	except:
		print("not yet")
		time.sleep(1)
		wait_for_influxdb(db_client)

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

	#Array of dictionaries that stores data on how much data was gathered in each ADC/Channel.
	#This will allow for variable amounts of data to be recieved and processed correctly
	data_points_entered = []

	for group in grouped.groups:
		adc, channel = group
		tags = dict(adc=adc, channel=channel)
		sub_df = grouped.get_group(group)[['mV']]

		#Add dictionary to array that stores information on which adc, channel, and how much data was published to the database with those tags
		data_points_entered.append(dict(adc=adc, channel=channel, amountOfData=len(sub_df)))

		db_client.write_points(sub_df, 'measurements', tags=tags)

	print('Data Written to DB')
	os.remove('received.csv')
	return data_points_entered

def main():
	"""
	MQTT Client connector in charge of receiving the 10 Hz csv files,
	perform calculations and store them in the database
	"""
	#influxdb information for connection -- right now is local
	db_host = 'localhost'#'influxdb' #'localhost'
	db_port = 8086
	db_username = 'root'
	db_password = 'root'
	database = 'testing'

	#info of the MQTT broker
	host = 'iot.eclipse.org'#"10.128.189.236" #'iot.eclipse.org'
	port = 1883
	keepalive = 30
	client_id = None #client_id is randomly generated

	#Add Location Topics to this array in order to allow for multiple publishers
	topic_locations = ["usa/quincy/1", "usa/quincy/2"]

	commsTopic = "communication/influxdbUpdate"

	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			# Callback for when the client receives a CONNACK response from the server.
			print("Connected with result code {}".format(rc))
			# Subscribes to topic with QoS 2

			#Subscribing to all publishers
			for topic in topic_locations:
				client.subscribe(topic, 2)
		else:
			print("Error in connection")

	def on_message(client, userdata, msg):
		# The callback for when a PUBLISH message is received from the server.
		#Detects an arriving message (CSV) and writes it in the db
		payload = msg.payload
		try:
			dataEnteredArray = write_to_db(payload, db_client)
			#Adding the location of the publisher to the information that will be sent to calculator
			locationAndDataArray = [msg.topic, dataEnteredArray]
			#Publishing index information on new data added to Influx to Calculator microservice
			client.publish(commsTopic, json.dumps(locationAndDataArray))
		except: #This needs to be changed
			print("Error")

	def on_publish(client, userdata, result):
		# Function for clients's specific callback when pubslishing message
		print("Comms Data Sent")
		pass

	# connects to database and creates new database
	db_client = DataFrameClient(host=db_host, port=db_port, username=db_username, password=db_password, database=database)
	# waits for influxdb service to be active
	wait_for_influxdb(db_client=db_client)
	db_client.create_database('testing')

	#Establish conection with broker and start receiving messages
	# Params -> Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
	# We set clean_session to False, so in case connection is lost, it'll reconnect with same ID
	# For debug purposes (client_id is not defined) we'll set it to True
	client = mqtt.Client(client_id=client_id, clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.on_publish = on_publish
	client.connect(host, port, keepalive)

	# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
	client.loop_forever()


if __name__ == '__main__':
	main()
