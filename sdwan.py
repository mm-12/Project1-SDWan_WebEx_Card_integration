import os
import requests




#to stop warrnings when doing get/post to https
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host, vmanage_port, vmanage_username, vmanage_password):
        api = "/j_security_check"
        base_url = f"https://{vmanage_host}:{vmanage_port}"
        url = base_url + api
        payload = {'j_username' : vmanage_username, 'j_password' : vmanage_password}
        
        print(url," ",payload)
        response = requests.post(url=url, data=payload, verify=False)
        print (response)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()
       
    @staticmethod
    def get_token(vmanage_host, vmanage_port, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None



#export vmanage_host=IP/FQDN
#export vmanage_port=port
#export vmanage_username=username
#export vmanage_password=password


vmanage_host = os.environ.get("vmanage_host")
vmanage_port = os.environ.get("vmanage_port")
vmanage_username = os.environ.get("vmanage_username")
vmanage_password = os.environ.get("vmanage_password")

print("url ", vmanage_host)
print("user ", vmanage_username)
print("pass ", vmanage_password)
base_url = f"https://{vmanage_host}:{vmanage_port}/dataservice"

api_logout_url = "/logout?nocache=1234"
base_logout_url = f"https://{vmanage_host}:{vmanage_port}"
url_logout = base_logout_url + api_logout_url

if vmanage_host is None or vmanage_port is None or vmanage_username is None or vmanage_password is None:
    print("some envs are missing. it is mandatory to set those env before running the app")
    exit()
        

def login():        
    # Login
    Auth = Authentication()
    jsessionid = Auth.get_jsessionid(vmanage_host,vmanage_port,vmanage_username,vmanage_password)
    token = Auth.get_token(vmanage_host,vmanage_port,jsessionid)
    print ("loging in is happening now")
    if token is not None:
        header = {'Content-Type': "application/json",'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
    else:
        header = {'Content-Type': "application/json",'Cookie': jsessionid}
    return header

def show_users(header):
    #random GET API for users list 

    url = base_url + "/admin/user"
    s=""

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        s= f"Failed to get list of users {str(response.text)}"
        return s


    for item in items:

        s=s+f"Username: {item.get('userName')} Group: {item.get('group')} Description: {item.get('description')}\n"

    print("printam show users")

    
    return s

def show_devices(header):
    #random GET API for device list 

    url = base_url + "/device"
    s=""

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        s= f"Failed to get list of devices {str(response.text)}"
        return s


    for item in items:
        s=s+f"Device ID: {item.get('deviceId')}\n"
    
    print("printam show devices")
    return s    


def show_controllers(header):
    #random GET API for controller list 

    url = base_url + "/system/device/controllers"
    s=""

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        s= f"Failed to get list of controllers {str(response.text)}"
        return s


    for item in items:
        s=s+f"Controller: {item.get('deviceType')}\n"
    
    print("printam show controllers")
    return s 

def show_vedges(header):
    #random GET API for vEdges list 

    url = base_url + "/system/device/vedges"
    s=""

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        s= f"Failed to get list of vEdges {str(response.text)}"
        return s

    for item in items:
        s=s+f"vEdge: {item.get('serialNumber')}\n"
    
    print("printam show vedges")
    return s

def show_bfd(header,deviceId):
    #random GET API for BFD  

    url = base_url + f"/device/bfd/sessions?deviceId={deviceId}"
    s=""

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        s= f"Failed to get BFD sessions {str(response.text)}"
        return s

    for item in items:
        s=s+f"BFD session: {item}\n"
    
    print("printam show bfd")
    return s

def show_ipsec(header,deviceId):
    #random GET API for IPSEC  

    url = base_url + f"/device/ipsec/outbound?deviceId={deviceId}"
    s=""

    response = requests.get(url=url, headers=header,verify=False)
    if response.status_code == 200:
        items = response.json()['data']
    else:
        s= f"Failed to get ipsec sessions {str(response.text)}"
        return s

    for item in items:
        s=s+f"IPSEC session: {item}\n"
    
    print("printam show bfd")
    return s

def logout(header):
    # Logout
    response = requests.get(url=url_logout, headers=header, verify=False,allow_redirects=False)
    print("logout is happening now")