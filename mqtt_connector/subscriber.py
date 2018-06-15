import paho.mqtt.client as mqtt
import pandas as pd
import numpy as np
from datetime import datetime

host = "35.237.36.219"
port = 1883
keepalive = 30

def ten_hz_client():
	"""
	MQTT Client connector in charge of receiving the 10 Hz csv files,
	perform calculations and store them in the database
	"""
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
	    with open('received.csv', 'wb') as fd:
	        fd.write(msg.payload)
	    df = pd.read_csv('received.csv')
	    df['mV'] = df['value']*0.125
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