#!/usr/bin/env python
import pika
import json
import subprocess
import hashlib


while 1:
	ip_list = ['172.26.169.103', '172.26.30.225', '172.26.83.6']
	for ip in ip_list:
		p = subprocess.check_output(["ping", "-c", "1", ip])
		print(ip)
		if p:
			con_consume = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
			channel_consume = con_consume.channel()
			con_publish = pika.BlockingConnection(pika.ConnectionParameters('172.26.99.35', 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
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
				
				case = json_msg["case"]
				
				if case == 1: # registration
					email = json_msg["email"]
					password = json_msg["password"].encode('utf-8')
					#salt = bcrypt.gensalt()
					#hashed = bcrypt.hashpw(password, salt)
					#hashed = str(hashed)[1:].replace("'", "")
					#hash_object = hashlib.md5(password)
					#hashed = hash_object.hexdigest()
					hashed = hash(password)
					firstName = json_msg["firstName"]
					lastName = json_msg["lastName"]
					insuranceId = json_msg["insuranceId"]
					query = f"INSERT INTO public.users(f_name, l_name, email, password, ins_id) VALUES ('{firstName}', '{lastName}', '{email}', '{hashed}', '{insuranceId}')"
				elif case == 2: # login
					email = json_msg["email"]
					password = json_msg["password"].encode('utf-8')
					#salt = bcrypt.gensalt()
					#hashed = bcrypt.hashpw(password, salt)
					#hashed = str(hashed)[1:].replace("'", "")
					#hash_object = hashlib.md5(password)
					#hashed = hash_object.hexdigest()
					hashed = hash(password)
					query = f"SELECT f_name, l_name, ins_id FROM public.users WHERE email='{email}' AND password='{hashed}'"
				elif case == 3: 
					insuranceId = json_msg["insuranceId"]
					specialty = json_msg["specialty"]
					#query = f"SELECT * FROM public.office"
					query = f"SELECT town, zip, state, phone, strt, off_name, doctor.f_name, doctor.l_name FROM public.office JOIN public.link ON link.ins_id='{insuranceId}' AND link.off_id=office.id JOIN public.doctor ON doctor.off_id=office.id AND doctor.specialty='{specialty}'"
				elif case == 4:
					officeId = json_msg['officeId']
					query = f"SELECT * FROM doctor WHERE off_id='{officeId}'"
				elif case == 5:
					oldEmail = json_msg["oldEmail"]
					updatePassword = json_msg["newPassword"].encode('utf-8')
					#salt = bcrypt.gensalt()
					#hashed = bcrypt.hashpw(password, salt)
					#hashed = str(hashed)[1:].replace("'", "")
					#hash_object = hashlib.md5(password)
					#hashed = hash_object.hexdigest()
					hashed = hash(password)
					updateIns = json_msg["newInsuranceId"]
					updateEmail = json_msg["newEmail"]
					#if (updatePassword==confirmPassword):
						#newPassword = updatePassword
					query = f"UPDATE public.users SET email='{updateEmail}', password='{hashed}', ins_id='{updateIns}' WHERE email='{oldEmail}'"
										
				channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
				print("Sent to db: " + query)
				#exec(open("send.py").read())
				consume_db()


			def callback(ch, method, properties, body):
				print(f'{body} is received from fe')
				send(body)

			channel_consume.basic_consume(queue="feTObe", on_message_callback=callback, auto_ack=True)

			channel_consume.start_consuming()
