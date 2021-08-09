from flask import Flask, request, json
import requests
from messenger import Messenger
#import sdwan
import re
from sdwan import Sdwan

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
                    print("Person ID ",data.get('data').get('personId'))
                    print("Raw msg: ",data.get('data'))
                    
                    # Collect the message id from the notification, 
                    # so you can fetch the message content or card content
                    messageId=data.get('data').get('id')
                    print("Message ID: ",messageId)
                    
                    # Get the type of the received message.
                    msg_type=data.get('data').get('type')
                    
                    # None for msg and submit for Card
                    print("MSG type: ",msg_type)
                    
                    # Get the content of the received message or card submitted.
                    if msg_type=="submit":
                        msg.get_card_message(messageId)
                        print("This is the submit content got from the webhook: ",msg.message_text)
                        print("this is the type of the submit got from the webhook: ", type(msg.message_text))
                        

                        # Final notification to send to as a response to webex teams
                        poruka = ""

                        sd = Sdwan()

                        for key,value in msg.message_text.items():
                            if value=="true":
                                if key=="0":
                                    poruka=sd.show_users()
                                    msg.post_message_card_output(roomId,poruka,"show users")
                                elif key=="1":
                                    poruka=sd.show_devices()
                                    msg.post_message_card_output(roomId,poruka,"show devices")
                                elif key=="2":
                                    poruka=sd.show_controllers()
                                    msg.post_message_card_output(roomId,poruka,"show controllers")
                                elif key=="3":
                                    poruka=sd.show_vedges()
                                    msg.post_message_card_output(roomId,poruka,"show vedges")
                        

                        if poruka == "":
                            poruka="None of the options selected. Try again!"
                            msg.post_message_roomId(roomId,poruka)
                       
                        sd.logout()
                        
                    else:
                        msg.get_txt_message(messageId)
                        print("This is the msg content got from the webhook: ",msg.message_text)
                        print("this is the type of the msg got from the webhook: ", type(msg.message_text))

                    

                        # If Hello is sent, show the cards
                        if "hello" in msg.message_text.lower():
                            msg.post_message_card_input(roomId,"Card")
                        else:
                            msg.post_message_roomId(roomId,"Type hello to start")
                    
                

                    '''
                    # Login to SDWAN and get proper header 
                    header=sdwan.login()

                    # Final notification to send to as a response to webex teams
                    poruka = ""
            
                    # If message received from webex teams has any of supported commands, call sdwan specific func.
                    if "show users" in msg.message_text:
                        poruka+=sdwan.show_users(header)
                    if "show devices" in msg.message_text:
                        poruka+=sdwan.show_devices(header)
                    if "show controllers" in msg.message_text:
                        poruka+=sdwan.show_controllers(header)
                    if "show vedges" in msg.message_text:
                        poruka+=sdwan.show_vedges(header)
                    
                    # Regex to check IPs (check python library for this too)
                    ips=re.findall(r"show bfd (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", msg.message_text)
                    print("if ip found in show bfd", ips)
                    if ips:
                        for ip in ips:
                            poruka+=sdwan.show_bfd(header,ip)
                    
                    # Regex to check IPs (check python library for this too)
                    ips=re.findall(r"show ipsec (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", msg.message_text)
                    print("if ip found in show ipsec", ips)

                    if ips:
                        for ip in ips:
                            poruka+=sdwan.show_ipsec(header,ip)

                    # If finall notification is still empty, it means that unsupported command was issued. Generate generic msg
                    if poruka == "":
                        poruka="Supported commands are: show users, show devices, show controllers, show vedges, show bfd <IP>, show ipsec <IP>"

                    # Logout from SDWAN
                    sdwan.logout(header)
                    
                    # Post a finall notification to webex teams 
                    msg.post_message_roomId(roomId,poruka)
                    '''
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


def create_webhook(url,resource):
    webhooks_api = f'{msg.base_url}/webhooks'
    data = { 
        "name": f"Webhook to ChatBot - {resource}",
        "resource": resource,
        "event": "created",
        "targetUrl": f"{url}"
        }
    webhook = requests.post(webhooks_api, headers=msg.headers, data=json.dumps(data))
    if webhook.status_code != 200:
        webhook.raise_for_status()
    else:
        print(f'Webhook to {url} created for ChatBot - {resource}')


def get_webhook_urls():
    webhook_urls_res = []
    webhooks_api = f'{msg.base_url}/webhooks'
    webhooks = requests.get(webhooks_api, headers=msg.headers)
    if webhooks.status_code != 200:
            webhooks.raise_for_status()
    else:
        for webhook in webhooks.json()['items']:
            webhook_urls_res.append((webhook['targetUrl'],webhook['resource']))
    return webhook_urls_res

ngrok_url="http://87780dcb5385.eu.ngrok.io"
ngrok_url_msg=[(ngrok_url,"messages")]
ngrok_url_att=[(ngrok_url,"attachmentActions")]

webhook_urls = get_webhook_urls()


print ("set msg: ", set(ngrok_url_msg))
print ("set att: ", set(ngrok_url_att))
print ("set urls: ", set(webhook_urls))

intersect_msg = list(set(ngrok_url_msg) & set(webhook_urls))
intersect_att = list(set(ngrok_url_att) & set(webhook_urls))

print ("intersect_msg: ",intersect_msg)

print ("intersect_att: ",intersect_att)


if intersect_msg:
    print(f'Registered webhook for Msg: {intersect_msg[0]}')
else: 
    create_webhook(ngrok_url, "messages")

if intersect_att:
    print(f'Registered webhook for Att: {intersect_att[0]}')
else: 
    create_webhook(ngrok_url, "attachmentActions")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
