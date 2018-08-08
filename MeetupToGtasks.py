#! C:\Users\mihai\AppData\Local\Programs\Python\Python36-32\python.exe
# MeetupToGtasks.py - gets list of attendees from Meetup and places them into Google Tasks

#Following quickstart procedures from Google API: https://developers.google.com/tasks/quickstart/python#troubleshooting
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#work with dates for Paypal transactions filtering
import datetime
from datetime import timedelta

#holds meetup connection
import meetup
#holds paypal connection
import paypal
#reads mapping
import pp_meetup_mapping


#Get Meetup attendees list
attendees = meetup.get_attendees()

#get today's date and find which day of the week it is
today_date = datetime.date.today()
today_index = today_date.weekday()

#get date for this week's monday and sunday
monday = str(today_date - timedelta(days=today_index))
sunday = str(today_date + timedelta(days=(6-today_index)))

#Get list of PayPal transactions between this week's monday and sunday 
transactions = paypal.get_transactions(monday, sunday)

#Read PayPal - Meetup mapping
mapping = pp_meetup_mapping.read_mapping('meetup_paypal_combo.csv')

#Create list of unmarked and unmapped payees
unmarked_payees = []
unmapped_payees = []

for transaction in transactions:	
	#check if value of payment is equal to 8 pounds
	payment = float(transaction['transaction_info']['transaction_amount']['value'])
	if payment == 8:
		payer = transaction['payer_info']['payer_name']['alternate_full_name']
		
		#if payer in mapping then add to payer list, if not add to unmapped list
		if payer in mapping:
			unmarked_payees.append(mapping[payer])
		else:
			unmapped_payees.append(payer)			

#ADD ATTENDEES TO GOOGLE TASKS

# Setup the Google Tasks API
SCOPES = 'https://www.googleapis.com/auth/tasks'
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('tasks', 'v1', http=creds.authorize(Http()))

# Create a tasklist that will hold the basketball attendees
tasklist_entry = {'title':'Bball - '+datetime.datetime.today().strftime('%d-%m')}
tasklist = service.tasklists().insert(body=tasklist_entry).execute()

# Add attendees one by one as tasks
for attendee in attendees:
	
	#Exclude the host (me) and "No" RSVPs
	if attendee["member"]["event_context"]["host"] or attendee['response'] == 'no':
		continue
		
	else:
		#add name of attendee to task
		task = {'title' : attendee["member"]["name"]}
		
		#if attendee paid then show him as completed
		if attendee['member']['name'] in unmarked_payees:
			task['status']='completed'
			unmarked_payees.remove(attendee['member']['name'])
			
		#add task to task list
		result = service.tasks().insert(tasklist=tasklist['id'], body=task).execute()
	
	#If attendee brings guests add them too one by one
	if attendee["guests"] > 0:
		for guest_number in range(attendee["guests"]):
			#Add them under same name as attendee who invited them, just with a + number (e.g. Alex + 1)
			task = {'title' : attendee["member"]["name"]+ " + " + str(guest_number+1)}
			result = service.tasks().insert(tasklist=tasklist['id'], body=task).execute()

#Print results
print('All attendees were copied!\n')

#Communicate if payees haven't been mapped
if unmarked_payees:
	print('Unmarked payees: ')
	for payee in unmarked_payees:
		print(payee)

print('\n')

#Communicate unmapped payees
if unmapped_payees:
	print('Unampped payees: ')
	for payee in unmapped_payees:
		print(payee)
