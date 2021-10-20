#!/usr/bin/env python
import pika 

print("reached send.py")
connection = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel = connection.channel()

def send_frontend(msg):
	channel.basic_publish(exchange='amq.direct',routing_key='c#TOfe',body=msg)
	print("sent to frontend")
	connection.close()

def callback_frontend(ch, method, properties, body):
	print(f'{body} is received')
	body = str(body)
	body = body[1:]
	body = body.replace("'", "")
	print(body)
	send_frontend(body)

channel.basic_consume(queue="postgresqlTOc#backend", on_message_callback=callback_frontend, auto_ack=True)

channel.start_consuming()
