#!/usr/bin/env python
import pika 

connection = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel = connection.channel()

def send(msg):
	channel.basic_publish(exchange='amq.direct',routing_key='c#TOfe',body=msg)
	print("sent to frontend")
	connection.close()

def callback(ch, method, properties, body):
	print(f'{body} is received')
	send(body)

channel.basic_consume(queue="postgresqlTOc#backend", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
