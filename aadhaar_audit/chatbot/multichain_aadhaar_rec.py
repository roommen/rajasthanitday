#!/usr/bin/env python
from flask import Flask, request
import time
import os
import json
import requests
import hashlib
# import pandas as pd
# import src.writeToDB as writeDB
# import src.authCode.authCodeGenerator as authcode
# from configurations.config import content

# Bot Framework Authorization
app = Flask(__name__)
auth_dict = {'code': """Bearer e7yd89jwio21njbhvwgedgyc789ueij3onjk2bhrfy7ewhdqoijswnkj2bh3vjerfgyewuhoidj"""}

def generatAuthCode():
	"""This function calls in the authentication codes for Microsoft Bot Framework"""
	auth_code = authcode.generateNewAccessToken()
	return auth_code

def text_msg_url_gen(service_url, cid):
	"""This function builds the service url to send a message to the chatbot"""
	service_url = '{0}/v3/conversations/{1}/activities/'.format(service_url, cid)
	return service_url

def build_text_message_payload(data, text):
	"""Creates a text message json payload, in which the chatbot reveives the message"""
	reply_text = text
	if data['channelId'] == 'webchat':
		x = "website_user"
	else:
		x = data['from']['name']
	payload = {
		'type': 'message',
		'from': {
			'id': data['recipient']['id'],
			'name': data['recipient']['name'],
		},
		'recipient': {
			'id': data['from']['id'],
			'name': x,
		},
		'text': reply_text,
		'replyToId': data['conversation']['id']
	}
	return payload

def send_to_conversation(service_url, payload):
	"""This function authorizes and makes a post request to the bot framework"""
	try:
		headers = {
			"Content-Type": "application/json",
			"Authorization": auth_dict['code'],
		}
		payload = json.dumps(payload)
		response = requests.post(service_url, data=payload, headers=headers)

		return response

	except Exception as e:
		print(e)
		pass

def check_num_string(msg):
	"""This function check if a 12 digit number string is given as user message, with/without strings"""
	try:
		num = msg.replace(' ','')
		int(num)
		if len(num)==12:
			return True
		else:
			return False
	except:
		return False

@app.route('/api/messages', methods=['GET', 'POST'])
def chat():
	if request.method.lower() == 'get':
		return "lol"
	else:
		data = request.json

		print('\n',data,'\n')

		# Generating an authentication code, specific to each bot framework
		auth_dict['code'] = generatAuthCode()

		# Check if the data sent to the chatbot is a text data and respond accordingly	
		if 'text' in data:
			auth_dict['code'] = generatAuthCode()

			print("Text message from user: ", data['text'],'\n')
			user_msg=data["text"]

			# print(reply)

			# Handling any greeting messages to the bot, and responding accordingly	
			if user_msg.lower() in ['hi','hello','hey']:
				print('Greeting detected')
				
				# Builds the payload to send a message to chatbot, with the required reply message
				payload = build_text_message_payload(data, 'Hi! Please enter your Aadhaar Number')

				# Builds the URL which will be required to send the message to chatbot
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])

				# Makes a post request to send a message to the chatbot, for the user
				x = send_to_conversation(service_url, payload)
				
				print("Send message to chat: ", x)

			# Detecting if the user has sent an Aadhaar number, 
			elif check_num_string(user_msg):
				print('Aadhaar number detected')

				# Making a json file to store the aadhaar number sent by the user
				with open('aadhaar_details_temp.txt', 'w') as outfile:
					json.dump(data, outfile)

				# Prompting the user for the OTP send on their registered mobile number
				payload = build_text_message_payload(data, 'Enter the OTP sent to your registered mobile number to authenticate')
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)

				print("Send message to chat: ", x)

			# Checking whether the OTP sent by the user matches the OTP.
			# Here it is a static 6-digit pass. No OTP system has be integrated.
			elif user_msg == '213289':

				print('OTP Correct')

				# Load the json file to fetch the aadhaar number sent by the user, to fetch details from the sample database
				with open('aadhaar_details_temp.txt', 'r') as f:
					datastore = json.load(f)

				# Encrypting the Aadhaar number in sha256 encoding sent by the user, for storing as a blockchain entry
				s = datastore['channelData']['text'].encode()
				m = hashlib.sha256()
				m.update(s)
				m1 = m.hexdigest()

				# Recording the current date time stamp for when the Aadhaar details of the user were accessed
				dts = time.strftime('%X %x %Z')
				cur_time = dts[:8]
				cur_date = cur_date = dts[12:14]+'/'+dts[9:11]+'/20'+dts[15:17]

				# This part gets the access to the UIDAI databse for fetching aadhaar details. In this case, it is just a csv file.
				aadf = pd.read_csv('AadhaarDB.csv')

				# Fetching all the details for the aadhaar number
				det = aadf[aadf["Aadhaar_Number"]==s].reset_index(drop=True)
				name = str(det.iloc[0,1]) + ' ' + str(det.iloc[0,2])
				gender = det.iloc[0,3]
				dob = det.iloc[0,4]
				address = det.iloc[0,5]


				payload = build_text_message_payload(data, 'Name:     '+name)
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)

				print("Send message to chat: ", x)

				payload = build_text_message_payload(data, 'DoB:       '+dob)
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)

				print("Send message to chat: ", x)

				payload = build_text_message_payload(data, 'Gender:   '+gender)
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)

				print("Send message to chat: ", x)

				payload = build_text_message_payload(data, 'Address:  '+address)
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)

				print("Send message to chat: ", x)

				# Since the access of aadhaar details of this user was detected, an entry to the blockchain stream is generated
				os.system("multichain-cli aadhaar publish demo '{\"app\": \"Skype AadhaarBot\",\"date\": \""+str(cur_date)+"\",\"time\": \""+str(cur_time)+"\",\"ip_addr\": \"103.203.139.3\",\"auth_type\": \"otp\"}' "+m1)				

		return 'message sent to user'

if __name__ == '__main__':
	app.debug = True #Uncomment to enable debugging
	app.run(port=1111) #Run the Server
