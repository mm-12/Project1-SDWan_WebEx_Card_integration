from flask import Flask, request, json
import requests
from messenger import Messenger
#import sdwan
import re
from sdwan import Sdwan
from jinja2 import Template


app = Flask(__name__)
port = 5005

msg = Messenger()
person_emails = ["mmiletic@cisco.com"]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'Content-Type' in request.headers and 'application/json' in request.headers.get('Content-Type'):
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
                # message received is card message
                msg.get_card_message(messageId)
                print("This is the submit content got from the webhook: ",msg.message_text)
                print("this is the type of the submit got from the webhook: ", type(msg.message_text))
                
                # need to check which button was pressed and based on that to show coresponding card

                print("PRITISNUTO JE: ", msg.message_text)

                
                if "main" in msg.message_text:
                    # Main menu card
                    if msg.message_text['button']=="new_network":
                        # Button new network
                        msg.post_message_card_input(roomId,"Card for new network", card("01_card_newNetwork.json"))
                    elif msg.message_text['button']=="show":
                        # Button show
                        msg.post_message_card_input(roomId,"Card for show commands", card("02_card_show.json"))
                    elif msg.message_text['button']=="backup":
                        # Button backup
                        msg.post_message_card_input(roomId,"Card for backup", card("03_card_backup.json"))

                elif "newnetwork" in msg.message_text:
                    # New network card
                    if msg.message_text['network']=="11":
                        # option 11
                        
                        vard={"var1": "Option 11 selected", "var2": "some output for option 11", \
                            "colour1": "Accent","colour2": "Good","colour3": "Dark"}

                        msg.post_message_card_output(roomId,"option 11", card("10_card_output_generic.json",vard))

                        print("izabrana opcija 11")
                    elif msg.message_text['network']=="22":
                        # option 22

                        vard={"var1": "Option 22 selected", "var2": "some output for option 22", \
                            "colour1": "Accent","colour2": "Good","colour3": "Dark"}

                        msg.post_message_card_output(roomId,"option 22", card("10_card_output_generic.json",vard))
                        print("izabrana opcija 22")
                    else:
                        print("Network not selected!")
                        
                        vard={"var1": "Nothing selected", "var2": "Please select at least one network", \
                            "colour1": "Attention","colour2": "Attention","colour3": "Attention"}

                        msg.post_message_card_output(roomId,"Nothing selected", card("10_card_output_generic.json",vard))


                elif "show" in msg.message_text:
                    # Show card
                    sd = Sdwan()
                    none_selected=True

                    if msg.message_text['show_users']=="true":
                        # show user = True 

                        vard={"var1": "Show user option selected", "var2": sd.show_users(), \
                            "colour1": "Accent","colour2": "Good","colour3": "Dark"}
                        
                        msg.post_message_card_output(roomId,sd.show_users(),card("10_card_output_generic.json",vard))

                        print("izabrana opcija show users")
                        none_selected=False
                    
                    if msg.message_text['show_devices']=="true":
                        # show devices = True

                        vard={"var1": "Show devices option selected", "var2": sd.show_devices(), \
                            "colour1": "Accent","colour2": "Good","colour3": "Dark"}

                        msg.post_message_card_output(roomId,sd.show_devices(),card("10_card_output_generic.json",vard))

                        print("izabrana opcija show devices")
                        none_selected=False

                    if msg.message_text['show_controllers']=="true":
                        # show controllers = True

                        vard={"var1": "Show controllers option selected", "var2": sd.show_controllers(), \
                            "colour1": "Accent","colour2": "Good","colour3": "Dark"}

                        msg.post_message_card_output(roomId,sd.show_controllers(),card("10_card_output_generic.json",vard))

                        print("izabrana opcija show controllers")
                        none_selected=False
                    
                    if none_selected:
                        # Nothing selected

                        print("Nothing selected")

                        vard={"var1": "None selected", "var2": "None of the show options selected. Please select at least one show output!", \
                            "colour1": "Attention","colour2": "Attention","colour3": "Attention"}

                        msg.post_message_card_output(roomId,sd.show_controllers(),card("10_card_output_generic.json",vard))



                elif "backup" in msg.message_text:
                    # Backup card
                    
                    
                    vard={"var1": "Backup option selected", "var2": "Backup is starting!!!", \
                        "colour1": "Accent","colour2": "Good","colour3": "Dark"}

                    msg.post_message_card_output(roomId,"backup",card("10_card_output_generic.json",vard))

                    print("start backup")
                    
                
            else:
                # message received is text message
                msg.get_txt_message(messageId)
                print("This is the msg content got from the webhook: ",msg.message_text)
                print("this is the type of the msg got from the webhook: ", type(msg.message_text))

            
                # If Hello is sent, show the cards
                if "hello" in msg.message_text.lower():
                    msg.post_message_card_input(roomId,"Card for main manu", card("00_card_menu.json"))
                else:
                    msg.post_message_roomId(roomId,"Type hello to start")           
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

        return data

    else: 
        msg_text = "We got GET or POST from CURL or something is wrong"
        for person_email in person_emails:
            msg.post_message_email(person_email, msg_text)
        return None


def card(card_file,vard=None):
    with open(f'Cards/{card_file}') as fp:
        text = fp.read()
    
    if vard:
       t = Template(text) 
       r= t.render(vard)

       return json.loads(r)
    else:
        return json.loads(text)

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

ngrok_url="http://faea97fe4531.eu.ngrok.io"
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
