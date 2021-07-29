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

# GET LIST OF DOMAINS + IPs + DATES, CHECK THEM AGAINST UMBRELLA, PROCESS THE
# EVENTS, AND UPLOAD THEM INTO CV

'''
This script integrates all of the previous modules. It starts with the list of domains that need to be checked, and finishes
by pushing the malicious ones into the CV Center.

Furthermore, this script is divided into 1 function:
- Funcion 1 (push_it_all()):
    DESCRIPTION: first, get the malicious domains from the original list of domains. For those domains that are malicious,
        the script processes the events (check process_events.py for more information), and then adds them to the domains DB
    INPUTS (2): list of domains, domains SB
    OUTPUTS (0): pushes all malicious domains into CV
'''

import requests
import json

# Import the functions from other scripts
from process_events import process_events
from get_domain_and_push_it import integration_process
from process_events import filter_malicious

file = open('domains_DB.json',)
domains_DB = json.load(file)

## FUNCTION
# Gets the list of domains, processes them, and upload them into CV
def push_it_all(domains_list, domains_DB):

    # Filter those domains that are not malicious
    malicious_list = filter_malicious(domains_list)

    # Check only if there are malicious/unknown DNS queries
    if not malicious_list:
        print("Nothing to process")
    else:
        # Processes the events depending on whether they have already been queried or not
        process_events(malicious_list, domains_DB)

        # Check list of domains with Umbrella, adds them to the DB
        integration_process(malicious_list, domains_DB)
    


# Example to test code
'''
example = [{"domain" : "google.com", "IP" : "1.1.1.1", "time" : "2021-04-22 16:00:00"},
           {"domain" : "umbrella.com", "IP" : "2.2.2.2", "time" : "2021-04-22 16:00:00"},
           {"domain" : "cisco.com", "IP" : "3.3.3.3", "time" : "2021-04-22 16:00:00"},
           {"domain" : "example.com", "IP" : "2.76.3.2", "time" : "2021-04-22 16:00:00"},
           {"domain" : "internetbadguys.com", "IP" : "24.54.87.71", "time" : "2021-07-22 17:00:00"}]
push_it_all(example, domains_DB)
'''