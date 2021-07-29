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

UMBRELLA = {
    "en_url": "https://s-platform.api.opendns.com/1.0/",
    "inv_url": "https://investigate.api.umbrella.com", 
    "inv_token": "<insert investigate token>",
    "en_key": "<insert enforcement_key>"
    }

CYBERVISION = {
    "base_url" : "<insert Cyber Vision url>",
    "x-token-id": "<insert Cyber Vision token>"

}

WHOISXML = {
    "apiKey": "<insert api key>",
    "base_url": "https://domain-reputation.whoisxmlapi.com/api/v1"
}

IPQUALITYSCORE = {
    "apiKey": "<insert api key>",
    "base_url": "https://ipqualityscore.com/api/json/url"
}

#ONLY CHECK FLOWS SEEN IN THE LAST X DAYS. eg, ( PERIOD = {'period':7})
# TYPE IN X AS AN INTEGER VALUE TO THE KEY 'period
#LEAVE THIS BLANK IF YOU'RE RUNNING THE SCRIPT FOR THE FIRST TIME OR IF YOU WANT TO RETRIEVE ALL DOMAINS SEEN IN CV
PERIOD = {'period':170}

# Time (in days) that needs to pass to push into CV a domain that has already been queried
time_between_queries = 7
