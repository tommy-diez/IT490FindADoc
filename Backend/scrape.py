#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json

def save_html(content, path):
	with open(path, mode='w', encoding='utf-8') as file:
		file.write(content)

url = 'https://www.horizonnjhealth.com/findadoctor/doctor/plan-horizon-nj-health/address-Newark,%20NJ%2007102,%20USA/specialty-All%20PCPs/sort-by-distance/sort-order-asc'
#'https://connect.werally.com/search/providers/07102/page-1?coverageType=medical&lat=40.74&long=-74.17&pf=t&propFlow=true&sort=distance&specialty=98'
#'https://doctorfinder.horizonblue.com/dhf_search/doctors/plan-garden+state+plan/distance-5/city-newark/state-nj/zip-07102/specialty-all+pcps/page-1/sub-category-all/criteria-all+primary+care+physicians+(pcps)/network-codes-oex1?application=dhf'
#'https://www.aetnabetterhealth.com/newjersey/find-provider?provsearch=true&name=&MedicalName=&city=&zip=07102&distance=25&county=&plan=&language=&specialty=Family+Practice%2cGeneral+Practice%2cMEDICINE%2cMULTI+PROVIDER+GROUP%2c&access=0&newpatient=0&affiliation=&groupaffiliation=&gender=&agesserved=&certified=0&Sorting=3&NumberofProviders=5&extendedHours=&accreditation=&extendedOfficesHours=&telemedicine=False&page=1'

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
addressList = []
for e in range(len(addresses)):
	addresses[e] = addresses[e].getText().replace('\t', '').split('\n')
	innerAddressList = []
	for j in range(len(addresses[e])):
		#print(str(j) + " " + addresses[e][j])
		if (j == 0 or j == 1 or j == 3):
			continue;
		elif (len(innerAddressList) == 2):
			addressList.append(innerAddressList);
			break;
		else:
			innerAddressList.append(addresses[e][j])
'''		
print(len(specialties))
for s in range(len(specialties)):
	#print(specialties[s].string)
	print("TEST #" + str(s) + ": " + str(specialties[s].string))
	#if (str(specialties[s].string) == 'None'):
		#temp_list = soup.select_one('div.search-results:nth-child(' + str(s) + ') > div > div > div > ul > li > a')
		#print(type(temp_list))
		#specialties[s] = temp_list.string
		#print(temp_list)
'''
			
#print(addressList)
			
print(len(addressList))
for i in range(len(names)):
	print("\nPerson " + str(i+1))
	print(names[i].string)
	print(phoneNumbers[i].string)
	print(addressList[i])
	#print(specialties[i].string)


save_html(soup.prettify(), 'page.txt')
# file = open('page.txt', mode='w', encoding='utf-8')
# file.write(soup.prettify())

