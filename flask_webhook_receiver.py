from flask import Flask, request, json
import requests
from messenger import Messenger
import sdwan
import re

app = Flask(__name__)
port = 5005
msg = Messenger()
person_emails = ["mmiletic@cisco.com", "wdaar@cisco.com"]


@app.route('/', methods=['GET', 'POST'])
def index():
    """Receive a notification from XXXXXX and handle it"""
    if request.method == 'GET':
        return(f'This GET request received on local port {port}')
    elif request.method == 'POST':
        if 'Content-Type' in request.headers:
            if 'application/json' in request.headers.get('Content-Type'):
                # Notification payload, received from XXXX webhook. Assuming there are all these fields below
                data = request.get_json()
                
                # Determine if POST came from SDWAN or WEBEX teams.
                if "data" in data:
                    #we got POST from Webex teams
                    print("post from webex teams")
                    
                    if msg.bot_id == data.get('data').get('personId'):
                        return 'Message from self ignored'
                    # Collect the roomId from the notification,
                    # so you know where to post the response
                    roomId=data.get('data').get('roomId')
                    print("Room ID: ",roomId)
                    print("Person ID ------ ",data.get('data').get('personId'))
                    print("Raw msg: ",data.get('data'))
                    # Collect the message id from the notification, 
                    # so you can fetch the message content
                    messageId=data.get('data').get('id')
                    print("Message ID: ",messageId)
                    # Get the contents of the received message.
                    msg_type=data.get('data').get('type')
                    print("MSG type: ",msg_type)
                    msg.get_message(messageId,msg_type)
                    print("This is the msg content got from webhook: ",msg.message_text)

                    if data.get('data').get('personId') == "Y2lzY29zcGFyazovL3VzL1BFT1BMRS85ZjRhZTNlNC0xMjY4LTRkODctYjE4ZS1lMzMwOTVmNDViYWQ":
                        poruka = "Igor thank you, you are such a wonderful bot... like real SNS bot "
                        msg.post_message_roomId(roomId,poruka)
                        return data
                    header=sdwan.login()

                    poruka = ""
            
                    # If message starts with '/xxxxx', relay it to the web server.
                    # If not, just post a confirmation that a message was received.
                    if "show users" in msg.message_text:
                        poruka=poruka+sdwan.show_users(header)
                    if "show devices" in msg.message_text:
                        poruka=poruka+sdwan.show_devices(header)
                    if "show controllers" in msg.message_text:
                        poruka=poruka+sdwan.show_controllers(header)
                    if "show vedges" in msg.message_text:
                        poruka=poruka+sdwan.show_vedges(header)
                    
                    ips=re.findall(r"show bfd (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", msg.message_text)
                    print(ips)
                    if ips:
                        for ip in ips:
                            poruka=poruka+sdwan.show_bfd(header,ip)

                    ips=re.findall(r"show ipsec (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", msg.message_text)
                    print(ips)
                    if ips:
                        for ip in ips:
                            poruka=poruka+sdwan.show_ipsec(header,ip)

                    if poruka == "":
                        poruka="Supported commands are: show users, show devices, show controllers, show vedges, show bfd <IP>, show ipsec <IP>"

                    sdwan.logout(header)
                    msg.post_message_roomId(roomId,poruka)
                
                else:
                    #we got POST from SDWAN
                    print("post sa SDWAN")
                
                    severity=data["severity"]
                    message=data["message"]
                    component=data["consumed_events"][0]["component"]
                    system_ip=data["consumed_events"][0]["system-ip"]
                    hostname=data["consumed_events"][0]["host-name"]
                    vpn_id=data["consumed_events"][0]["vpn-id"]
                    # Print the notification payload, received from the webhook
                    print(json.dumps(data,indent=4))
                    #msg_text = "We got POST from SDWAN"
                    msg_text=f"Severity: {severity} from hosname: {hostname} with IP: {system_ip} and VPN ID: {vpn_id}, on COMPONENT: {component} with the message:\n{message}"
                    for person_email in person_emails:
                        msg.post_message_email(person_email, msg_text)

                return  data

            else: 
                return ('Wrong data format', 400)
        else:
            msg_text = "We got POST from curl"
            for person_email in person_emails:
                msg.post_message_email(person_email, msg_text)
            return ('CURL request')


def create_webhook(url):
    webhooks_api = f'{msg.base_url}/webhooks'
    data = { 
        "name": "Webhook to ChatBot",
        "resource": "messages",
        "event": "created",
        "targetUrl": f"{url}"
        }
    webhook = requests.post(webhooks_api, headers=msg.headers, data=json.dumps(data))
    if webhook.status_code != 200:
        webhook.raise_for_status()
    else:
        print(f'Webhook to {url} created')

def get_webhook_urls():
    webhook_urls = []
    webhooks_api = f'{msg.base_url}/webhooks'
    webhooks = requests.get(webhooks_api, headers=msg.headers)
    if webhooks.status_code != 200:
            webhooks.raise_for_status()
    else:
        for webhook in webhooks.json()['items']:
            webhook_urls.append(webhook['targetUrl'])
    return webhook_urls

ngrok_url=["http://87780dcb5385.eu.ngrok.io"]

webhook_urls = get_webhook_urls()

print (webhook_urls)
print (ngrok_url)
intersect = list(set(ngrok_url) & set(webhook_urls))

print (intersect)
if intersect:
    print(f'Registered webhook: {intersect[0]}')
else: 
    create_webhook(ngrok_url[0])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
