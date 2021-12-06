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
specialty = 'Pediatrics'
insurance = 'Horizon'
policy = 'Horizon NJ Health'

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
	print(zip_codes[i]) '''


save_html(soup.prettify(), 'page.txt')
# file = open('page.txt', mode='w', encoding='utf-8')
# file.write(soup.prettify())


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
			
			'''
			def loop_offices():
				

			def consume_from_insurance_select_1(): # get reponse from select query sent to insurance table to see if the insurance exists
				channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_from_insurance_select, auto_ack=True)
				
			def consume_from_insurance_select_2(): # get reponse from select query sent to insurance table to see if the insurance exists
				channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback_from_insurance_select, auto_ack=True)
			
			def consume_from_insurance_insert():
				channel_consume.basic_consume(queue="dbTObe", on_message_callback=send_select_to_insurance_2, auto_ack=True)

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
				if body != "": # if it doesn't exist
					query = f"INSERT INTO public.insurance(ins_name, policy) VALUES ('{insurance}', '{policy}')"
					send_insert_to_insurance(query)
				else:
					# to office loop
				
				# need parsing of db message to send true/false to frontend for success for login/register
				

			def callback(ch, method, properties, body):
				print(f'{body} is received from fe')
				send(body)
				
			def send_select_to_insurance_1(fmsg): # first step
				query = f"SELECT ins_id FROM public.insurance WHERE ins_name='{insurance}' AND policy='{policy}'"
				channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
				print("Sent to db: " + query)
				#exec(open("send.py").read())
				consume_from_insurance_select_1()
				
			def send_select_to_insurance_2(fmsg): # check
				query = f"SELECT ins_id FROM public.insurance WHERE ins_name='{insurance}' AND policy='{policy}'"
				channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
				print("Sent to db: " + query)
				#exec(open("send.py").read())
				consume_from_insurance_select_2()

			channel_consume.basic_consume(queue="dbTObe", on_message_callback=callback, auto_ack=True)

			channel_consume.start_consuming()
			'''
			
			def test_callback_from_insurance_select(ch, method, properties, body):
				print(f'Received from db: {body}')
				body = str(body)
				body = body[1:]
				body = body.replace("'", "")
				print(body)
				if body != "": # if it doesn't exist
					print("It doesn't exist")
				else:
					print("It exists") # to office loop
				
				# need parsing of db message to send true/false to frontend for success for login/register
			
			def test_consume_from_insurance_select_1(): # get reponse from select query sent to insurance table to see if the insurance exists
				channel_consume.basic_consume(queue="dbTObe", on_message_callback=test_callback_from_insurance_select, auto_ack=True)
			
			def test_send_select_to_insurance_1(): # first step
				query = "SELECT ins_id FROM public.insurance WHERE ins_name='test' AND policy='123'"
				channel_publish.basic_publish(exchange='amq.direct',routing_key='beTOdbRK',body=query)
				print("Sent to db: " + query)
				#exec(open("send.py").read())
				test_consume_from_insurance_select_1()
				
			test_send_select_to_insurance_1()
			
