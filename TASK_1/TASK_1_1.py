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

# THIS SCRIPT AGGREGATES ALL OF THE ACTIONS AND SCRIPTS THAT ARE NEEDED TO
# CHECK THE DOMAINS AGAINST UMBRELLA

import json

# Import functions from other scripts
from retrieve_urls import retrieve_urls
from get_DNS_queries import get_DNS_queries
from push_it_all import push_it_all

# MAIN
print("Starting the code...")

# This function retrieves the complete list of requested domains, with their
# associated IP and date when this ocurred
retrieve_urls()
print("Step 1/4: Domains have been retrieved successfully.")

# This function reads the content inside domains_urls.json and stores it into
# a Python dictionary
domains_list = get_DNS_queries()
print("Step 2/4: Domains have been obtained successfully from JSON file.")

# Get information from the Database of domains
file = open('domains_DB.json',)
domains_DB = json.load(file)
print("Step 3/4: Information has been successfully obtained from DB.")

# This function processes the requests made previously, and pushes them into
# CV if necessary
push_it_all(domains_list, domains_DB)
print("Step 4/4: New domains have been successfully processed and pushed to CV.")