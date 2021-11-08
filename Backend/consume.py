#!/usr/bin/env python
import pika
import json

con_consume = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel_consume = con_consume.channel()
con_publish = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel_publish = con_publish.channel()

def consume_db():
	channel_consume.basic_consume(queue="postgresqlTOc#backend", on_message_callback=callback_frontend, auto_ack=True)

def send_frontend(msg):
	channel_publish.basic_publish(exchange='amq.direct',routing_key='c#TOfe',body=msg)
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
		query = "INSERT INTO public.users(f_name, l_name, email, password, ins_id) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, 1), {'firstName': firstName, 'lastName': lastName, 'email': email, 'password': password}"
	else:
		query = "SELECT f_name, l_name FROM public.users WHERE email=%(email)s AND password=%(password)s, {'email': email, 'password': password}"
		
	channel_publish.basic_publish(exchange='amq.direct',routing_key='c#TOdb',body=query)
	print("Sent: " + query)
	#exec(open("send.py").read())
	consume_db()


def callback(ch, method, properties, body):
	print(f'{body} is received')
	send(body)

channel_consume.basic_consume(queue="nodejsTOc#backend", on_message_callback=callback, auto_ack=True)

channel_consume.start_consuming()
