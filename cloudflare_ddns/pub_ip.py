import requests
import json
import socket
from datetime import datetime
import os
from dotenv import load_dotenv


def __init__():
    __author__ = "jwsundance"

def cloudflare_dns_api(pubaddress):
        load_dotenv()
        zone_id = os.getenv('ZONE')
        record_id = os.getenv('RECORD')
        api_token = os.getenv('TOKEN')
        a_record = os.getenv('A_RECORD')
        x_auth_email = os.getenv('EMAIL')
        todays_date = datetime.now()
        #zone_id = located in .env file as ZONE
        #record_id = located in .env file as RECORD
        #api_token = located in .env file as TOKEN
        #a_record = located in .env file as A_RECORD
        #x_auth_email = located in .env file as EMAIL
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

        payload = {
            "content": pubaddress,
            "name": f"{a_record}",
            "proxied": False,
            "type": "A",
            "comment": f"{todays_date}",
            "ttl": 1
        }
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Email": f"{x_auth_email}",
            "x-Auth-Key": f"{api_token}"
        }

        #response =
        requests.request("PATCH", url, json=payload, headers=headers)

        #print(response.text)

def pub_ip() -> str:
    try:
        url2 = "https://api.ipify.org?format=json"
        myip = requests.get(url2)
        status_code = myip.status_code
        response = json.loads(myip.text)


    except Exception as error:
        print(f"Failure || {error}")

    pubaddress = response["ip"]
    #print(pubaddress)
    return pubaddress


def nslookup_ip() -> str:
    load_dotenv()
    a_record = os.getenv('A_RECORD')
    dns_ip = socket.gethostbyname(a_record)
    #print (dns_ip)
    return dns_ip


def diff_ns_ip(pubaddress, dns_ip):
    todays_date = datetime.now()
    if pubaddress == dns_ip:
        print (f"{todays_date} IPs are the same")
        pass
    else:
        cloudflare_dns_api(pubaddress)
        print(f"Change to public IP {pubaddress}")

if __name__ == "__main__":

    pubaddress = pub_ip()
    dns_ip = nslookup_ip()
    diff_ns_ip(pubaddress, dns_ip)
