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

# USE UMBRELLA INVESTIGATE API TO GET DOMAIN REPUTATION

'''
This script gathers the Umbrella url and token in order to authenticate an be able to use the Umbrella Investigate API

Furthermore, this script is divided into 3 functions:
- Funcion 1 (check_errors()):
    DESCRIPTION: given the status code of an API request, it prints an error if it has not been successful
    INPUTS (1): status code
    OUTPUTS (0): prints a message

- Function 2 (get_reputation()):
    DESCRIPTION: first, it makes an API request to the Umbrella API to get all of the information that
        it can gather regarding a specific DNS query/domain. It stores this information in the "query" dictionary. Afterwards,
        it makes a new API call to get the Risk Score of the particular domain, and also stores it in the "query" dictionary
    INPUTS (1): domain/DNS query
    OUTPUTS (1): "query" dictionary

- Function 3 (get_reputation_list()):
    DESCRIPTION: leverages the get_reputation() function to perform the Umbrella checks in a list of domains, instead of a
        specific one
    INPUTS (1): list of domains to be checked
    OUTPUTS (1): list of responses for each domain
'''

import requests
import json
import env
from pprint import pprint

# Retrieve the base URL and the token for authorization
base_url = env.UMBRELLA["inv_url"]
API_token = env.UMBRELLA["inv_token"]


## FUNCTION
# Checks for errors in API request
def check_errors(status_code):
    if status_code != 200:
        print("Error " + str(status_code) + " in the API Request")

## FUNCTION
# Makes Umbrella Investigate API to check the DNS queries
def get_reputation(domain):
    query = {}

    # API call for CATEGORIZATION
    url = base_url + "/domains/categorization/" + domain + "?showLabels"
    headers = {"Authorization": "Bearer " + API_token}
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
        
    # Check for possible Request errors
    check_errors(response.status_code)

    # Get relevant Umbrella outputs
    query["url_status"] = response_json[domain]["status"]
    query["url_security_categories"] = response_json[domain]["security_categories"]
    query["url_contentcategories"] = response_json[domain]["content_categories"]
    

    # API call for RISK SCORE
    url = base_url + "/domains/risk-score/" + domain
    headers = {"Authorization": "Bearer " + API_token}
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)

    # Check for possible Request errors
    check_errors(response.status_code)

    # Extract relevant information from Umbrella
    query["url_risk_score"] = response_json["risk_score"]

    # Add domain that we are talking about
    query["domain"] = domain

    return query


## FUNCTION
# Run DNS checking in multiple DNS queries
def get_reputation_list(domain_list):
    umbrella_response = []

    for item in domain_list:
        # Get output from Umbrella for each DNS domain
        query = get_reputation(item["domain"])
        
        # Store Umbrella response in Python dictionary
        umbrella_response.append(query)

    return umbrella_response


# Example to test code
'''
# Test code to check functions
domain = "internetbadguys.com"
response = get_reputation(domain)
pprint(response)
'''