"""
Copyright (c) 2021 Cisco and/or its affiliates.

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

""" 
The script searches the Umbrella investigate API for malicious domains 
associated with the input public IPv4 address, there is no current IPv6 
functionality.  
Script input is a list of dictionaries containing a key 'ip' where the 
IPv4 address resides, and 'firstActivity' where the address was first 
seen. 
The output is a returned list of dictionaries containing the IP, first 
activity, and malicious domains associated with the IP. 
The is additionally written to a .json file. If there are no malicious 
domains the output returns an empty list. 
"""

import requests 
import json 
import env as config

# Returns a list of malicious domains associated with a given IPv4 
# address. 
def umbrella_ip_to_dom(ipList):
    base_url = config.UMBRELLA["inv_url"]
    headers = {
        "Authorization" : "Bearer " + config.UMBRELLA["inv_token"],
        "Content-Type" : "application/json"
    }

    malicious_ips = []

    # Error checking the API get method that retrieves malicious domains 
    # for an IPv4 address, raises issues associated with the Investigate 
    # API key.
    for p in ipList:
        response = requests.get(url=base_url+"/ips/"+p['ip']+
                                "/latest_domains",headers=headers, 
                                verify=False)
        if response.status_code != 200:
            print("Error "+str(response.status_code)+" Encountered")
            if response.status_code==403 or 401:
                print("Please Check to Ensure The right Investigate API key is set on the env file")
            pass
        else:
            data = response.json()
            # If the array is empty no malicious domains have been found
            if len(data) == 0:
                print("HTTP Response: " + str(response.status_code) + 
                    ", IP: " + str(p['ip']) + " has no domains listed as malicious by Umbrella")

            # If the array is populated these are appended to a list of 
            # dictionaries that include IP, domains and first activity
            else:
                malicious_domains = []
                for m in data:
                    malicious_domains.append(m['name'])
                malicious_ips.append({'IP' : str(p['ip']), 'domains' : malicious_domains, 'time' : str(p['firstActivity'])})
        
        # Written to a file
        with open('mal_domains.json', 'w') as f:
            f.write(json.dumps(malicious_ips, indent=2)) 

    # Malicious domains returned for use in the TASK_2 main script
    return malicious_ips