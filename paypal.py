#requests helps with API call and authentication
import requests
from requests.auth import HTTPBasicAuth
import keys


#universal credentials
client_id = keys.pp_client_id
secret = keys.pp_secret

def get_token():
	"""Get PayPal token for API connection"""	
	
	#set up API call for token
	url = 'https://api.paypal.com/v1/oauth2/token'
	headers_pp = {'Accept':'application/json','Accept-Language': 'en_US'}
	login_pp = HTTPBasicAuth(client_id, secret)
	data_pp = {'grant_type':'client_credentials'}

	#get token
	return requests.post(url, headers=headers_pp, \
		data=data_pp, auth = login_pp).json()['access_token']

def get_transactions(start_date, end_date):
	"""Get list of transactions occurring between start_date and end_date variables"""
	
	token = get_token()
	
	#Set up API call for Paypal transactions
	url = 'https://api.paypal.com/v1/reporting/transactions?start_date=' + \
		start_date + 'T00:00:00-0700&end_date=' + end_date + 'T00:00:00-0700&fields=payer_info'
	headers_paypal = {'Content-Type':'application/json','Authorization':'Bearer '+token}

	#Get list of Paypal transactions
	return requests.get(url, headers=headers_paypal).json()['transaction_details']
