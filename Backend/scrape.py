#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json
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


save_html(soup.prettify(), 'page.txt')
# file = open('page.txt', mode='w', encoding='utf-8')
# file.write(soup.prettify())

'''
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
				
				switch(i) {
					case 1:
						email = json_msg["email"]
						password = json_msg["password"]
						firstName = json_msg["firstName"]
						lastName = json_msg["lastName"]
						insuranceId = json_msg["insuranceId"]
						query = f"INSERT INTO public.users(f_name, l_name, email, password, ins_id) VALUES ('{firstName}', '{lastName}', '{email}', '{password}', '{insuranceId}')"
						break;
					case 2:
						email = json_msg["email"]
						password = json_msg["password"]
						query = f"SELECT f_name, l_name FROM public.users WHERE email='{email}' AND password='{password}'"
						break;
					case 4:
						officeId = json_msg['officeId']
						query = f"SELECT * FROM doctor WHERE off_id='{officeId}'";
						break;
					case 5:
						updatePassword = json_msg["password"]
						confirmPassword = json_msg["confirmPassword"]
						updateIns = json_msg["insuranceId"]
						updateEmail = json_msg["email"]
						if (updatePassword==confirmPassword):
							newPassword = updatePassword
						query = f"UPDATE public.users SET email='{updateEmail}', password='{newPassword}', ins_id='{updateIns}' WHERE email='session variable sent from tom'";
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
'''
