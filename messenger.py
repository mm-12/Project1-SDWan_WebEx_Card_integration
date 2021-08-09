import json
import requests
from cardjson import card_input
from cardjson import card_output


# API Key is obtained from the Webex Teams developers website.
api_key = 'NmVkYzY3ZmEtYmIwYi00MGEwLWI5YmEtNzQ3ZmQyZTFlNjFlMTRkMjA4MjEtOTBj_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
# Webex Teams messages API endpoint
base_url = 'https://webexapis.com/v1'

class Messenger():
    # When init Messanger class prepare url, key, headers, bot_id
    def __init__(self, base_url=base_url, api_key=api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.bot_id = requests.get(f'{self.base_url}/people/me', headers=self.headers).json().get('id')


    # RETRIVE A MESSAGE
    # Retrieve a specific message posted by user -> str, using message_id
    def get_txt_message(self, message_id): 
        received_message_url = f'{self.base_url}/messages/{message_id}'
        self.message_text = requests.get(received_message_url, headers=self.headers).json().get('text')

    # Retrieve a specific card submitted by  user -> dict, using message_id
    def get_card_message(self, message_id):
        received_message_url = f'{self.base_url}/attachment/actions/{message_id}'
        self.message_text =requests.get(received_message_url, headers=self.headers).json().get('inputs')
      
    
    # POST A MESSAGE
    # Post a message to a Webex Teams space (to email address send a message)
    def post_message_email(self, person_email, message):
        data = {
            "toPersonEmail": person_email,
            "text": message,
            }
        post_message_url = f'{self.base_url}/messages'
        requests.post(post_message_url,headers=self.headers,data=json.dumps(data))

    # Post a message to a Webex Teams space (to roomId send a message)
    def post_message_roomId(self, room_id, message):
        data = {
            "roomId": room_id,
            "text": message,
            } 
        post_message_url = f'{self.base_url}/messages'
        requests.post(post_message_url,headers=self.headers,data=json.dumps(data))

    # Post a card to a Webex Teams space (to roomID post an input card)
    def post_message_card_input(self, room_id, message):
        data = {
            "roomId": room_id,
            "text": message,
            "attachments": card_input
            } 
        post_message_url = f'{self.base_url}/messages'
        requests.post(post_message_url,headers=self.headers,data=json.dumps(data))

    #Post a card to a Webex Teams space (to roomID post an output card/result card)
    def post_message_card_output(self, room_id, message, command):
        # Output card location of a command
        card_output[0]['content']['body'][0]['columns'][1]['items'][1]['text']=command
        # Output card location of an output to print
        card_output[0]['content']['body'][1]['text']=message
        data = {
            "roomId": room_id,
            "text": message,
            "attachments": card_output
            } 
        post_message_url = f'{self.base_url}/messages'
        requests.post(post_message_url,headers=self.headers,data=json.dumps(data))
