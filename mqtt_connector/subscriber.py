import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime
from influxdb import DataFrameClient

def ten_hz_client():
	"""
	MQTT Client connector in charge of receiving the 10 Hz csv files,
	perform calculations and store them in the database
	"""
	#influxdb information for connection -- right now is local
	db_info = {
		'host' : 'localhost',
		'port' : 8086,
		'username' : 'root',
		'password' : 'root',
		'database' : 'foo',
	}

	#creating an influxdb client instance
	db_client = DataFrameClient(host=db_info['host'], port=db_info['port'], username=db_info['username'], password=db_info['password'], database=db_info['database'])

	#info of the MQTT broker
	host = "35.237.36.219"
	port = 1883
	keepalive = 30
	client1_id = "ENC_Connector"
	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(client1, userdata, flags, rc):
	    print("Connected with result code {}".format(rc))
	# Subscribing in on_connect() means that if we lose the connection and reconnect then 
	# subscriptions will be renewed.
	    client1.subscribe("RasPi1/10Hz", 2)

	# The callback for when a PUBLISH message is received from the server.
	def on_message(client1, userdata, msg):
	    print("received message")
	    #create new file and write the received msg on it
	    with open('received.csv', 'wb') as fd:
	        fd.write(msg.payload)
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


	    df.to_csv('updated.csv', index=False)

	# Params -> Client(client_id=””, clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)
	# We set clean_session False, so in case connection is lost, it'll reconnect with same ID
	client1 = mqtt.Client(client_id=client1_id, clean_session=False)
	client1.on_connect = on_connect
	client1.on_message = on_message

	client1.connect(host, port, keepalive)

	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	client1.loop_forever()

if __name__ == '__main__':
	ten_hz_client()