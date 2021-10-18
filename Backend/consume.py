#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel = connection.channel()
connection2 = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel2 = connection2.channel()
def send_frontend(msg):
	channel2.basic_publish(exchange='amq.direct',routing_key='c#TOfe',body=msg)
	print("sent to frontend")

def callback_frontend(ch, method, properties, body):
	print(f'{body} is received')
	body = str(body)
	body = body[1:]
	body = body.replace("'", "")
	print(body)
	send_frontend(body)

def send(fmsg):
	json_msg = json.loads(fmsg)
	print(json_msg["email"] + " " + json_msg["password"])
	
	email = json_msg["email"]
	password = json_msg["password"]
	
	if json_msg.keys() >= {"firstName","lastName"}:
		firstName = json_msg["firstName"]
		lastName = json_msg["lastName"]
		query = f"INSERT INTO public.users(f_name, l_name, email, password, ins_id) VALUES ('{firstName}', '{lastName}', '{email}', '{password}', 1)"
	else:
		query = f"SELECT * FROM public.users WHERE email={email} AND password={password}"
		
	channel.basic_publish(exchange='amq.direct',routing_key='c#TOdb',body=query)
	print("Sent: " + query)
	#exec(open("send.py").read())
	channel2.basic_consume(queue="postgresqlTOc#backend", on_message_callback=callback_frontend, auto_ack=True)
	channel2.start_consuming()
	


def callback(ch, method, properties, body):
	print(f'{body} is received')
	send(body)

channel.basic_consume(queue="nodejsTOc#backend", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
