import requests
import keys

#Meetup API key
key = keys.meetup

def get_attendees():
	
	"""gets list of attendees"""
	#API call to meetup that gets event id
	url = 'https://api.meetup.com/East-London-Basketball-Group/events?\
		key='+key+'&&sign=true&photo-host=public&page=20'
	event_id = requests.get(url).json()[0]['id']
	
	#API call to meetup that gets attendees
	url = 'https://api.meetup.com/East-London-Basketball-Group/events/'+\
		event_id+'/rsvps?key=' + key + '&sign=true&photo-host=public'
	
	return requests.get(url).json()
