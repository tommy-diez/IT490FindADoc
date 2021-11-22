#!/usr/bin/env python
import pika
import json


while 1:
	ip_list = ['172.26.169.103', '172.26.30.225', '172.26.83.6']
	for ip in ip_list:
		p = subprocess.check_output(["ping", "-c", "1", ip])
		print(ip)
		if p:
			con_consume = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
			channel_consume = con_consume.channel()
			con_publish = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
			channel_publish = con_publish.channel()

			def consume_db():
				channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_frontend, auto_ack=True)

			def send_frontend(msg):
				channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOfeRK',body=msg)
				print("sent to frontend")

			def callback_frontend(ch, method, properties, body):
				print(f'{body} is received from db')
				body = str(body)
				body = body[1:]
				body = body.replace("'", "")
				print(body)
				
				# need parsing of db message to send true/false to frontend for success for login/register
				
				send_frontend(body)

			def send(fmsg):
				json_msg = json.loads(fmsg)
				# print(json_msg["email"] + " " + json_msg["password"])
				
				i = json_msg["case"]
				
				switch(i){
					case 0:
						email = json_msg["email"]
						password = json_msg["password"]
						firstName = json_msg["firstName"]
						lastName = json_msg["lastName"]
						insuranceId = json_msg["insuranceId"]
						query = f"INSERT INTO public.users(f_name, l_name, email, password, ins_id) VALUES ('{firstName}', '{lastName}', '{email}', '{password}', '{insuranceId}')"
						break;
					case 1:
						email = json_msg["email"]
						password = json_msg["password"]
						query = f"SELECT f_name, l_name FROM public.users WHERE email='{email}' AND password='{password}'"
						break;
					case 2:
						query = "";
						break;
					case 3:
						query = "";
						break;
					case 4:
						query = "";
						break;
					case 5:
						query = "";
						break;
										
				channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
				print("Sent to db: " + query)
				#exec(open("send.py").read())
				consume_db()


			def callback(ch, method, properties, body):
				print(f'{body} is received from fe')
				send(body)

			channel_consume.basic_consume(queue="feTObe", on_message_callback=callback, auto_ack=True)

			channel_consume.start_consuming()
