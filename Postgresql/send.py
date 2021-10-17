#!/usr/bin/env python
import pika 

connection = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel = connection.channel()

channel.basic_publish(exchange='amq.direct',routing_key='postgresql',body='Test from postgresql send.py')

connection.close()
