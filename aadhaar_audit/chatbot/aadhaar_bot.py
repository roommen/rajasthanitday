#!/usr/bin/env python
from flask import Flask, request
import time
import os
import json
import requests
import hashlib
import src.authCode.authCodeGenerator as authcode
import pandas as pd
# import src.writeToDB as writeDB
from configurations.config import content

# Bot Framework Authorization
app = Flask(__name__)
auth_dict = {'code': """Bearer e7yd89jwio21njbhvwgedgyc789ueij3onjk2bhrfy7ewhdqoijswnkj2bh3vjerfgyewuhoidj"""}

def generatAuthCode():
	auth_code = authcode.generateNewAccessToken()
	return auth_code

def text_msg_url_gen(service_url, cid):
	"""build the service url"""
	service_url = '{0}/v3/conversations/{1}/activities/'.format(service_url, cid)
	return service_url

def build_text_message_payload(data, text):
	"""Creates a text only message dict"""
	#reply_text = model.callme(text, data['conversation']['id'])
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
	#print payload
	return payload

def send_to_conversation(service_url, payload):
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
		return "Jatan"
	else:
		data = request.json

		print('\n',data,'\n')

		auth_dict['code'] = generatAuthCode()

		if data['type'] == 'contactRelationUpdate':
			print("A new user has added the bot")
			auth_dict['code'] = generatAuthCode()
			payload = build_text_message_payload(data, content['welcomeText'])

			service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
			a = generatAuthCode()

			requests.post(service_url, data=json.dumps(payload), headers={"Content-Type": "application/json","Authorization": a,})

			#send_to_conversation(service_url, payload)

		if data['type'] == 'endOfConversation':
			print("############################ end of conversation ################################")

		# if data['type'] == 'message':
		if 'text' in data:
			auth_dict['code'] = generatAuthCode()
			# with open('helloworld.txt', 'w') as outfile:
			# 	json.dump(data, outfile)

			print("Text message from user: ", data['text'],'\n')
			user_msg=data["text"]

			# print(reply)

			if user_msg.lower() in ['hi','hello','hey']:
				print('Greeting detected')
				payload = build_text_message_payload(data, 'Hi! Please enter your Aadhaar Number')
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)
				
				print("Send message to chat: ", x)


			elif check_num_string(user_msg):
				print('Aadhaar number detected')
				with open('aadhaar_details_temp.txt', 'w') as outfile:
					json.dump(data, outfile)
				payload = build_text_message_payload(data, 'Enter the OTP sent to your registered mobile number to authenticate')
				service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
				x = send_to_conversation(service_url, payload)

				print("Send message to chat: ", x)

			elif user_msg == '213289':

				print('OTP Correct')

				with open('aadhaar_details_temp.txt', 'r') as f:
					datastore = json.load(f)

				s = datastore['channelData']['text'].encode()
				m = hashlib.sha256()
				m.update(s)
				m1 = m.hexdigest()

				dts = time.strftime('%X %x %Z')
				cur_time = dts[:8]
				cur_date = cur_date = dts[12:14]+'/'+dts[9:11]+'/20'+dts[15:17]
				
				if datastore['channelData']['text'] == '123423453456':

					payload = build_text_message_payload(data, 'Name:     Bruce Wayne')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'DoB:      12/06/1982')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'Gender:   Male')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'Address:  Wayne Manor, Gotham')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					os.system("multichain-cli aadhaar publish demo '{\"app\": \"skype aadhaarbot\",\"date\": \""+str(cur_date)+"\",\"time\": \""+str(cur_time)+"\",\"ip_addr\": \"103.203.139.3\",\"auth_type\": \"otp\"}' "+m1)	

				if datastore['text'] == '345698766789':
					
					payload = build_text_message_payload(data, 'Name:     Diana Prince')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'DoB:      18/03/1904')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'Gender:   Female')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'Address:  Amazon')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

				if datastore['text'] == '789065431234':
					
					payload = build_text_message_payload(data, 'Name:     Clark Kent')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'DoB:      15/07/1988')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'Gender:   Male')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

					payload = build_text_message_payload(data, 'Address:  The Daily Planet, Metropolis')
					service_url = text_msg_url_gen(data['serviceUrl'], data['conversation']['id'])
					x = send_to_conversation(service_url, payload)

					print("Send message to chat: ", x)

		return 'message sent to user'


if __name__ == '__main__':
	app.debug = True #Uncomment to enable debugging
	app.run(port=1234) #Run the Server
