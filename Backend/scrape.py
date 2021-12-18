#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import pika
import json
import os
import subprocess
import re

global states
states = ['IA', 'KS', 'UT', 'VA', 'NC', 'NE', 'SD', 'AL', 'ID', 'FM', 'DE', 'AK', 'CT', 'PR', 'NM', 'MS', 'PW', 'CO', 'NJ', 'FL', 'MN', 'VI', 'NV', 'AZ', 'WI', 'ND', 'PA', 'OK', 'KY', 'RI', 'NH', 'MO', 'ME', 'VT', 'GA', 'GU', 'AS', 'NY', 'CA', 'HI', 'IL', 'TN', 'MA', 'OH', 'MD', 'MI', 'WY', 'WA', 'OR', 'MH', 'SC', 'IN', 'LA', 'MP', 'DC', 'MT', 'AR', 'WV', 'TX']

def save_html(content, path):
	with open(path, mode='w', encoding='utf-8') as file:
		file.write(content)

url = 'https://www.horizonnjhealth.com/findadoctor/doctor/plan-horizon-nj-health/address-Newark,%20NJ%2007102,%20USA/specialty-Pediatrics/sort-by-distance/sort-order-asc/page-6'
global specialty
global insurance
global policy
specialty = '1'
insurance = 'Horizon'
policy = 1

#'https://www.horizonnjhealth.com/findadoctor/doctor/plan-horizon-nj-health/address-Newark,%20NJ%2007102,%20USA/specialty-All%20PCPs/sort-by-distance/sort-order-asc'


# Making a GET request
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# check status code for response received
# success code - 200
print(r.status_code)

# print request content
# print(soup.prettify)


names = soup.select('div.search-results > div > div > strong > a')
officeNames = soup.select('div.search-results > div > div > address > strong')
#specialties = soup.select('div.search-results > div > div > div > ul > li')
phoneNumbers = soup.select('div.search-results > div > div > address > div > span')
addresses = soup.select('div.search-results > div > div > address')
firstNames = []
lastNames = []
addressList = []
cities = []
states = []
zip_codes = []
for e in range(len(addresses)):
	current_name = names[e].string.split(",")[0].split(" ")
	firstNames.append(current_name[0])
	if len(current_name) == 3:
		lastNames.append(current_name[2])
	else:
		lastNames.append(current_name[1])
	addresses[e] = addresses[e].getText().replace('\t', '').split('\n')
	for j in range(len(addresses[e])):
		#print(str(j) + " " + addresses[e][j])
		if (j == 0 or j == 1 or j == 3):
			continue;
		elif (j == 2):
			addressList.append(addresses[e][j])
		elif (j == 4):
			values = addresses[e][j].split(", ")
			cities.append(values[0])
			#regex = re.compile(r'\b(' + '|'.join(states) + r')\b')
			#states.append(regex.match(values[1]).group())
			state = values[1].split(" ")[0]
			states.append(state)
			zip_codes.append(values[1].replace(state, "").replace(" ", ""))
			
			
#print(addressList)
	
		'''	
print(len(addressList))
for i in range(len(names)):
	print("\nPerson " + str(i+1))
	print(firstNames[i])
	print(lastNames[i])
	print(phoneNumbers[i].string)
	print(officeNames[i].string)
	print(addressList[i])
	print(specialty)
	print(cities[i])
	print(states[i])
	print(zip_codes[i]) 
'''

save_html(soup.prettify(), 'page.txt')
# file = open('page.txt', mode='w', encoding='utf-8')
# file.write(soup.prettify())

#global ins_id
#global isLoopDone
#global curr_index # index of current office in loop


ip_list = ['172.26.169.103', '172.26.30.225', '172.26.83.6']
for ip in ip_list:
	p = subprocess.check_output(["ping", "-c", "1", ip])
	print(ip)
	if p:
		con_consume = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
		channel_consume = con_consume.channel()
		con_publish = pika.BlockingConnection(pika.ConnectionParameters('172.26.99.35', 5672, '/', pika.PlainCredentials('findadoc', 'Findadoc!')))
		channel_publish = con_publish.channel()
		
		
		def send_insert_to_doctor(off_id):
			f_name = firstNames[curr_index]
			l_name = lastNames[curr_index]
			query = f"INSERT into public.doctor (f_name, l_name, off_id, specialty) values ('{f_name}', '{l_name}', '{off_id}', '{specialty}')"
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
			print("Sent to db: " + query)
			isLoopDone = True
		
		def send_insert_to_link(ch, method, properties, body):
			print(f'Received from db: {body}')
			body = str(body)
			body = body[1:]
			body = body.replace("'", "")
			print(body) # this should be the off_id as this is the callback from the 2nd select after inserting an office
			off_id = body
			query = f"INSERT into public.link (ins_id, off_id) values ('{ins_id}', '{off_id}')"
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
			print(f"Sent to db: {query}")
			send_insert_to_doctor(off_id)
					
		def consume_from_office_select_2():
			channel_consume.basic_consume(queue="dbTObe", on_message_callback=send_insert_to_link, auto_ack=True)
		
		def send_select_to_office_2(): # get off_id now that office is inserted to use in inserting to link table
			office = officeNames[curr_index].string
			query = f"SELECT id from public.office where name='{office}'"
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
			print("Sent to db: " + query)
			consume_from_office_select_2() # consume response
		
		def callback_select_office_2(ch, method, properties, body):
			send_select_to_office_2()
		
		def consume_from_office_insert():
			channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_select_office_2, auto_ack=True)
		
		def send_insert_to_office(msg):
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=msg)
			print(f"Sent to db: {msg}")
			consume_from_office_insert()
		
		def callback_from_office_select(ch, method, properties, body):
			print(f'Received from db: {body}')
			body = str(body)
			body = body[1:]
			body = body.replace("'", "")
			print(body)
			if body == "Error": # if it doesn't exist
				street = addressList[curr_index]
				city = cities[curr_index]
				state = states[curr_index]
				zip_code = zip_codes[curr_index]
				name = officeNames[curr_index].string
				query = f"INSERT INTO public.office(street, town, zip, state, phone, name) VALUES ('{street}', '{city}', '{zip_code}', '{state}', '{name}')"
				send_insert_to_office(query)
			else: # if does it exists
				off_id = body # get the off_id to use when inserting to the link table later
				send_insert_to_doctor(off_id) # add the doctor
			
			# need parsing of db message to get ins_id to put in the link table later
		
		def consume_from_office_select():
			channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_from_office_select, auto_ack=True)
		
		def send_select_to_office(): # check if office exists
			office = officeNames[curr_index].string
			query = f"SELECT id from public.office where name='{office}'"
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
			print("Sent to db: " + query)
			consume_from_office_select() # consume response
		
		def loop_offices():
			for i in range(len(officeNames)):
				global curr_index
				curr_index = i
				global isLoopDone
				isLoopDone = False
				send_select_to_office()
				#while not isLoopDone:
					#print("******")
	
		def callback_to_select_insurance(ch, method, properties, body):
			send_select_to_insurance()
		
		def consume_from_insurance_insert():
			channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_to_select_insurance, auto_ack=True)
		
		def send_insert_to_insurance(msg):
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=msg)
			print(f"Sent to db: {msg}")
			consume_from_insurance_insert()
		
		def callback_from_insurance_select(ch, method, properties, body):
			print(f'Received from db: {body}')
			body = str(body)
			body = body[1:]
			body = body.replace("'", "")
			print(body)
			if body == "Error": # if it doesn't exist
				query = f"INSERT INTO public.insurance(ins_name, policy) VALUES ('{insurance}', '{policy}')"
				send_insert_to_insurance(query)
			else: # if it does exist
				global ins_id
				ins_id = body # get the ins_id to use when inserting to the link table later
				loop_offices() # to office loop
			
			# need parsing of db message to get ins_id to put in the link table later

		def consume_from_insurance_select(): # get reponse from select query sent to insurance table to see if insurance exists
			channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_from_insurance_select, auto_ack=True)
			channel_consume.start_consuming()
			
		#1: start here
		def send_select_to_insurance(): # first step
			query = f"SELECT id FROM public.insurance WHERE ins_name='{insurance}' AND policy='{policy}'"
			channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
			print("Sent to db: " + query)
			consume_from_insurance_select()

		send_select_to_insurance()
		
		#def callback(ch, method, properties, body):
			#print("started consuming")

		#channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback, auto_ack=True)
		#channel_consume.start_consuming()
			
