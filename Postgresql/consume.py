#!/usr/bin/env python
import pika
import psycopg2
import os
import subprocess

while 1:
	ip_list = ['172.26.169.103', '172.26.30.225', '172.26.83.6']
	for ip in ip_list:
		p = subprocess.check_output(["ping", "-c", "1", ip])
		print(ip)
		if p:
			connection = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
			channel = connection.channel()
			def connect(msg):
				conn = None
				try:
					print('Connecting to DB')
					conn = psycopg2.connect(host="localhost", database="it490_db", user="postgres", password="password")

					cur = conn.cursor()
					SQL=cur.mogrify(msg)
					print(SQL)
					print('^what will be executed^')
					cur.execute(SQL)
					conn.commit()
					print('commit to db, if no db msg will produce error')
					try:
						db_msg = cur.fetchmany()
						db_msg=str(db_msg)
						channel.basic_publish(exchange='amq.direct',routing_key='dbTObeRK',body=db_msg)
						print(db_msg)
					except:
						channel.basic_publish(exchange='amq.direct',routing_key='dbTObeRK',body='Inserted Into Database')
				except (Exception, psycopg2.DatabaseError) as error:
					print('error')
					channel.basic_publish(exchange='amq.direct',routing_key='dbTObeRK',body='Error')
				finally:
					if conn is not None:
						conn.close()
						cur.close()
						print('Database connection closed.')


			def callback(ch, method, properties, body):
				print(f'{body} is received')
				connect(body)
			try:
				channel.basic_consume(queue='beTOdb', on_message_callback=callback, auto_ack=True)
				channel.start_consuming()
			except Exception as e:
				print("Connection to ",ip," lost")
		else:
			print(f"DOWN {ip} Ping Unsuccsessful")
