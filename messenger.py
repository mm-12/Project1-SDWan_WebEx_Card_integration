import json
import requests
from cardjson import card_input


# API Key is obtained from the Webex Teams developers website.
api_key = 'NmVkYzY3ZmEtYmIwYi00MGEwLWI5YmEtNzQ3ZmQyZTFlNjFlMTRkMjA4MjEtOTBj_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
# Webex Teams messages API endpoint
base_url = 'https://webexapis.com/v1'

class Messenger():
    def __init__(self, base_url=base_url, api_key=api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.bot_id = requests.get(f'{self.base_url}/people/me', headers=self.headers).json().get('id')

    def get_txt_message(self, message_id):
        """ Retrieve a specific message, specified by message_id """
        print(f'MESSAGE ID: {message_id}')
 
        received_message_url = f'{self.base_url}/messages/{message_id}'
        self.message_text = requests.get(received_message_url, headers=self.headers).json().get('text')
        
    def get_submit_message(self, message_id):
        """ Retrieve a specific message, specified by message_id """
        print(f'MESSAGE ID: {message_id}')
        
        received_message_url = f'{self.base_url}/attachment/actions/{message_id}'
        print(received_message_url)
        resp=requests.get(received_message_url, headers=self.headers)
        print(resp.json())
        self.message_text = resp.json().get('inputs')
        print(self.message_text)
      
       


    def post_message_email(self, person_email, message):
        """ Post message to a Webex Teams space, specified by room_id """
        data = {
            "toPersonEmail": person_email,
            "text": message,
            }
        post_message_url = f'{self.base_url}/messages'
        post_message = requests.post(post_message_url,headers=self.headers,data=json.dumps(data))
        print("raw reposnse when posting msg: ",json.dumps(post_message.json(),indent=4))

    def post_message_roomId(self, room_id, message):
        """ Post message to a Webex Teams space, specified by room_id """

        data = {
            "roomId": room_id,
            "text": message,
            } 
        post_message_url = f'{self.base_url}/messages'
        post_message = requests.post(post_message_url,headers=self.headers,data=json.dumps(data))
        print("raw reposnse when posting msg: ",json.dumps(post_message.json(),indent=4))

    def post_message_card(self, room_id, message):
        """ Post a card to a Webex Teams space, specified by room_id """

        data = {
            "roomId": room_id,
            "text": message,
            "attachments": card_input
            } 
        post_message_url = f'{self.base_url}/messages'
        post_message = requests.post(post_message_url,headers=self.headers,data=json.dumps(data))
        print("raw reposnse when posting msg: ",json.dumps(post_message.json(),indent=4))
