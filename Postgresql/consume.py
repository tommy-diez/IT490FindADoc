#!/usr/bin/env python
import pika
import psycopg2 

connection = pika.BlockingConnection(pika.ConnectionParameters('172.26.169.103', 5672, '/', pika.PlainCredentials('admin', 'Luftwaffe1')))
channel = connection.channel()
def connect(fmsg):
	conn = None
	try:
		temp=str(fmsg)
		msg=temp[1:]
		#msg=msg.replace("'", "")
		msg=msg.replace("\"", "")
		print('First msg: ',msg)


		print('Connecting to DB')
		conn = psycopg2.connect(host="localhost", database="it490_db", user="postgres", password="password")

		cur = conn.cursor()
		print(msg)
		cur.execute(msg)
		db_msg = cur.fetchone()
		db_msg=str(db_msg)
		channel.basic_publish(exchange='amq.direct',routing_key='postgresql',body=db_msg)
		print(db_msg)
		cur.close()

	except (Exception, psycopg2.DatabaseError) as error:
		print('error')
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')


def callback(ch, method, properties, body):
	print(f'{body} is received')
	connect(body)

channel.basic_consume(queue="c#backendTOpostgresql", on_message_callback=callback, auto_ack=True)

channel.start_consuming()
