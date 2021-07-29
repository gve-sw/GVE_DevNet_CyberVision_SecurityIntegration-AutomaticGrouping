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
Malicious domains are gathered from IPv4 addresses found flowing between
components detected within CV. 
The IPv4 address, domain, and first activity are logged and if this is
the initial viewing it is pushed as an event to CV and the database of domains is updated.
The flows searched are defined within the period given in env.py, in 
days from the current date. 
"""

# Import functions from other scripts
import json
from get_DNS_queries import get_DNS_queries
from push_it_all import push_it_all
from get_cv_ip import get_ips
from ip_get_domain import umbrella_ip_to_dom

# MAIN
print("Starting the code...")

# This function retrieves a list of public addresses witnessed by CV 
# and the date when this occurred.
public_ips = get_ips()
print("Step 1/4: IPv4 address gathering for the defined period has been completed.")

# This function searches the umbrella database for malicious domains 
# associated with the public addresses retrieved by the previous function.
malicious_domains = umbrella_ip_to_dom(public_ips)
domains_list = []

for a in malicious_domains:
    for b in a['domains']:
        domains_list.append(
            {
                'domain' : b, 
                'IP' : a['IP'], 
                'time' : a['time']
            }
        )

print("Step 2/4: The domain search has been completed.")
if len(domains_list) == 0:
    print("No malicious domains found, no further action needed.")
    print("Program complete.")
else:
    # Get information from the Database of domains
    file = open('domains_DB.json',)
    domains_DB = json.load(file)
    print("Step 3/4: Information has been successfully obtained from DB.")

    # This function processes the requests made previously, and pushes
    # them into CV if necessary
    push_it_all(domains_list, domains_DB)
    print("Step 4/4: The new malicious domains have been successfully processed and pushed to CV.")
    print("Program complete.")
