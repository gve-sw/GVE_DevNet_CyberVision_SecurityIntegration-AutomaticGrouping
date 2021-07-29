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

# INTEGRATION OF QUERYING UMBRELLA + "PROCESSING" THE EVENTS

'''
This script integrates the reputation gathered from Umbrella with the processing of the events. The word "processing" here
means adding the DNS query into the domains_DB, which is the json file that includes the malicious domains that have been queried

This script is divided into 3 functions:
- Funcion 1 (store_info()):
    DESCRIPTION: stores the modified information of the domains in a separate json file (that constantly updates itself)
    INPUTS (1): Python structure that contains the information about the domains

- Function 2 (get_position()):
    DESCRIPTION: gets the index position of a specific domain inside the domains_DB structure, which is the data coming from the json file
        that contains the information about the domains, IPs, and dates (the reason will be better understood in the integration_process() function)
    INPUTS (2): domain that wants to be checked, domains_DB
    OUTPUTS (1): index position of the specific domain

- Function 3 (integration_process()):
    DESCRIPTION: first, it checks whether this is the first time that the malicious domain has been queried. If it is, the domain is added as a new
        one into the database. If it is not, the database is updated with the new information
    INPUTS (2): domain to be treated, domains_DB
    OUTPUTS (1): add information from the new domain into the domains_DB structure (and consequently the json file)
'''

import requests
import json
from pprint import pprint

# Import the functions from other scripts
from get_reputation import get_reputation

def check_domain(domain, domains_DB):

    # Assume that it is the first time queried, set the variable to 1 (YES)
    first_time = 1
    for item in domains_DB:
        if item["domain"] == domain:
            # If the DNS has been queried previously, set the variable to 0 (NO)
            first_time = 0

    return first_time

file = open('domains_DB.json',)
domains_DB = json.load(file)

## FUNCTION
# Store the domain, IP and date in the database (domains_DB file)
def store_info(domains_DB):
    with open("domains_DB.json", "w") as file:
        json.dump(domains_DB, file, ensure_ascii=False, indent=4)

## FUNCTION
# Get the index position of the domain that has been repeated
def get_position(domain, domains_DB):
    i = 0
    for item in domains_DB["list"]:
        if domain == item["domain"]:
            index = i
        i = i + 1
    return index


## FUNCTION
def integration_process(domains_list, domains_DB):
    for item in domains_list:
        first_time_appeared = check_domain(item["domain"], domains_DB["list"])
        
        # First time that this domain has appeared
        if first_time_appeared == 1:
            # Get reputation from Umbrella, for the specific domain
            reputation = get_reputation(item["domain"])
            
            # Store the domain, IP and date in the dictionary
            new_domain = {}
            new_domain["domain"] = item["domain"]
            new_domain["count"] = 1
            new_domain["queries"] = []
            payload = {"IP" : item["IP"], "time" : item["time"]}
            new_domain["queries"].append(payload)

            domains_DB["list"].append(new_domain)

        # NOT the first time that this domain has appeared
        elif first_time_appeared == 0:
            # Determine position of domain that is repeated
            position = get_position(item["domain"], domains_DB)

            domains_DB["list"][position]["count"] = domains_DB["list"][position]["count"] + 1
            payload = {"IP" : item["IP"], "time" : item["time"]}
            domains_DB["list"][position]["queries"].append(payload)

        else:
            print("Error inside the code, please check!")

        store_info(domains_DB)