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

# UPLOAD ONLY THE INFORMATION THAT IS RELEVANT FOR THE USER

'''
This script pushes only the relevant information to CV Center

Furthermore, this script is divided into 3 functions:
- Funcion 1 (check_domain()):
    DESCRIPTION: given a domain and the domains database, it returns whether it has been previously queried or not
    INPUTS (2): domain to query, domains database
    OUTPUTS (1): returns a 1 if it is the 1st time seen, a 0 otherwise

- Function 2 (process_events()):
    DESCRIPTION: first, it determines if it is the 1st time that the malicious domain has been queried. If it is the case,
        it gets the information from Umbrella and uploads it into CV. If not, it will not do anything (this is subject to 
        change in future versions)
    INPUTS (1): list of malicious domains, domains DB
    OUTPUTS (0): push/not push the domain

- Function 3 (filter_malicious()):
    DESCRIPTION: given a list of  domains, it determines which domains are malicious/unknown (and therefore sohuld be pushed
        into CV), and which ones are not (and are ignored)
    INPUTS (1): list of domains to be checked
    OUTPUTS (1): list of domains that need to be sent to CV
'''

import requests
import json
import datetime

# Import the functions from other scripts
from create_event import CV_event
from get_reputation import get_reputation
from push_events import push_events
from get_domain_and_push_it import get_position

file = open('domains_DB.json',)
domains_DB = json.load(file)


## FUNCTION
# Checks whether the domain has been previously checked
# domains_DB is the list of domains (in a database) that have already been queried
def check_domain(domain, domains_DB):

    # Assume that it is the first time queried, set the variable to 1 (YES)
    first_time = 1
    for item in domains_DB:
        if item["domain"] == domain:
            # If the DNS has been queried previously, set the variable to 0 (NO)
            first_time = 0

    return first_time


# FUNCTION
# Given a DNS domain and its associated IP, make the decision of whether to push it or not
# into CV Center, based on previous Events
def process_events(malicious_list, domains_DB):
    for item in malicious_list:

        first_time_appeared = check_domain(item["domain"], domains_DB["list"])
        print("Checking domain " + item["domain"] + " ...")
        
        if first_time_appeared == 1:
            print("Domain " + item["domain"] + " has never appeared. Domain pushed to Cyber Vision\n")
            # Get reputation from Umbrella
            reputation = get_reputation(item["domain"])

            # Create message to upload to CV
            reputation["IP"] = item["IP"]
            reputation["Date"] = item["time"]
            payload = CV_event(reputation)

            # Push event into CV
            push_events(payload)

        elif first_time_appeared == 0:
            # print(item["domain"] + " already appeared!!\n")

            # Get index position of domain
            index = get_position(item["domain"], domains_DB)

            # Get timestamp for current event
            current_time = datetime.datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.datetime.timestamp(current_time)

            # Get timestamp for last event
            size = len(domains_DB["list"][index]["queries"]) - 1
            last_time = datetime.datetime.strptime(domains_DB["list"][index]["queries"][size]["time"], "%Y-%m-%d %H:%M:%S")
            last_time = datetime.datetime.timestamp(last_time)

            # Time difference in timestamp
            delta_time = current_time - last_time

            # Get time_between_queries from the configuration file and convert to seconds
            from env import time_between_queries
            time_between_queries = time_between_queries * 24 * 60 * 60

            # Set condition for posting the event in CV
            if delta_time > time_between_queries:
                # We need to post the event into CV
                time_between_queries = str(time_between_queries / 24 / 60 / 60)
                print("Domain " + item["domain"] + " already appeared. Domain pushed to Cyber Vision as more than " + time_between_queries + " days have passed.\n")
                # Get reputation from Umbrella
                reputation = get_reputation(item["domain"])

                reputation["IP"] = item["IP"]
                reputation["Date"] = item["time"]

                # Create message to upload to CV
                payload = CV_event(reputation)

                # Push event into CV
                push_events(payload)
            else:
                time_between_queries = str(time_between_queries / 24 / 60 / 60)
                print("Domain " + item["domain"] + " already appeared. Domain not pushed to Cyber Vision as less than " + time_between_queries + " days have passed.\n")

        else:
            print("The code is not functioning properly. Please check!")

## FUNCTION
# Gets the list of DNS queries, and outputs only the malicious/unknown ones
def filter_malicious(domains_list):
    malicious_list = []

    print("Filtering domains...")
    
    i = 0
    for item in domains_list:
        umbrella_response = get_reputation(item["domain"])

        if umbrella_response["url_status"] == -1: # The domain is malicious
            malicious_list.append(domains_list[i])
        elif umbrella_response["url_status"] == 0: # The domain is unknown
            malicious_list.append(domains_list[i])
        
        i = i + 1
        

    return malicious_list