"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

""" Retrieves the DNS records from Cyber Vision 
This script uses the function retrieve_urls() to retrieve all components and their flows from Cyber Vision.
Then it creates a json file and also returns the same dictionary with all of the domains, the last time they were accessed, and the IP address.
"""


import requests
import json
from env import *
from datetime import datetime
base_url = CYBERVISION.get("base_url")
token = CYBERVISION.get('x-token-id')
components_url = base_url+"/components"



headers = {
  'x-token-id': token
}


check_period = PERIOD.get('period')
current_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
current_date = datetime.strptime(current_date, "%Y/%m/%d %H:%M:%S")
dns_server_components=[]
dns_flows = []

mydict= {'domain':'', 'time':'', 'IP':''}
mylist=[]


#This functin converts a timestamp to a readable date/time value
def convert_to_time(timestamp):
    timestamp = str(timestamp)
    timestamp = int(timestamp[0 :10])
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object

#The FUNCTION BELOW :
#   1. Retrieves all components
#   2. Retrieves The Flows for Components with DNS_SERVER tags
#   3. Gets the Flows with DNS tag and gets the domains question in those flows (with IPs and time first Seen), and saves them in a JSON file.
#   4. The function returns a list of dictionaries, each dictionary containing a domain, its time and associated IP address

def retrieve_urls_ALL():

    components = requests.get(components_url, headers = headers, verify= False)

    if components.status_code == 200:
    
        for c in components.json():   
                    if  c['tags']: 
                        if c['tags'][0]['id'] == "DNS_SERVER":
                            dns_server_components.append(c['id'])

        # Get the flows for Each Component with DNS Server Tag
        for component in dns_server_components:
                flow_url = components_url+"/"+component+"/flows"
                response = requests.get(flow_url, headers = headers, verify = False)
                
                for flow in response.json():
                    if flow['tags']:
                        if flow['tags'][0]['id']=='DNS':
                            dns_flows.append(flow['id'])

        # For each flow with DNS tag, capture the domain queried, ip and time for First activity
        for flow in dns_flows:
            url = base_url+"/flows/"+flow
            resp = requests.get(url, headers = headers, verify = False)
            mydict['domain']=resp.json()['properties'][0]['value']
            mydict['IP']=resp.json()['left']['ip']
            time = convert_to_time(resp.json()['firstActivity'])
            mydict['time']= str(time)
            mylist.append(mydict.copy())

            with open("domains_urls.json", "w") as f:
                f.write(json.dumps(mylist, indent=2))
                f.close()
            
    
        return mylist
    else:
        print("HTTP Error",components.status_code, "ENCOUNTERED")



#The FUNCTION BELOW :
#  works almost similarly to the one above, However, this one records only flows within a Specified duration. 
# The user specifies Period they want in the env file.


def periodic_retrieve_urls():
    
        components = requests.get(components_url, headers = headers, verify= False)

        if components.status_code == 200:
            for c in components.json():   
                        if  c['tags']: 
                            if c['tags'][0]['id'] == "DNS_SERVER":
                                dns_server_components.append(c['id'])

            # Get the flows for Each Component with DNS Server Tag
            for component in dns_server_components:
                    flow_url = components_url+"/"+component+"/flows"
                    response = requests.get(flow_url, headers = headers, verify = False)
                    
                    for flow in response.json():
                        if flow['tags']:
                            if flow['tags'][0]['id']=='DNS':
                                dns_flows.append(flow['id'])

            # For each flow with DNS tag, capture the domain queried, ip and time for First activity
            for flow in dns_flows: 
                url = base_url+"/flows/"+flow
                resp = requests.get(url, headers = headers, verify = False)

                time = convert_to_time(resp.json()['firstActivity'])
                activity_time = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
                # Time difference between the current time and the time of the flow as retrieved from CV.
                time_diff = current_date - activity_time

                if time_diff.days <= check_period:

                    mydict['domain']=resp.json()['properties'][0]['value']
                    mydict['IP']=resp.json()['left']['ip']
                    mydict['time']= str(time)
                    mylist.append(mydict.copy())

                    with open("domains_urls.json", "w") as f:
                        f.write(json.dumps(mylist, indent=2))
                        f.close()
                
            return mylist
        else:
            print("HTTP Error",components.status_code, "ENCOUNTERED")


def retrieve_urls():
    if check_period:
        if str(check_period).isdigit():
            periodic_retrieve_urls()
        else:
            print("\nERROR ENCOUNTERED\nPlease check the value Entered on the env file to ensure it's an integer\n")
            pass
    else:
        retrieve_urls_ALL()


#Before Calling Any of the above functions to retrieve domains from CV, we check whether the user specified the Period.
#If the period is specified, we call the second function, periodic_retrieve_urls(), to get just specific urls
#Else, we call the retrieve_urls_all, which retrieves all domains from CV

#retrieve_urls()