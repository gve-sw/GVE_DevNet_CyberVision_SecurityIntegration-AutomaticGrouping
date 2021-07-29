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

""" Helper script for automated_grouping.py

This script includes different get calls that are made to the CyberVision API and used for the automated grouping:
- make_secure_api_call: make API call with errorhandling
- get_comp_no_groups: retrieves a list all ungrouped components
- get_ungrouped_components_vendors: retrieves a list of the vendors that the ungrouped components have

"""

import json
import requests
import env as config 

base_url = config.CYBERVISION["base_url"]
my_token = config.CYBERVISION["x-token-id"]

headers = {
    "x-token-id" : my_token
}

def make_secure_api_call(url, headers = {}):
    """ Make API call with error handling
    Parameters
    ----------
    url: str
        The url to make the api call
    headers: dict
        The headers used in the api call
    """
    try:
        response = requests.get(url, headers = headers, verify = False)
        if response.status_code == 429:
            print("You have exceeded the number of API calls allowed")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    return response

def get_comp_no_groups():
    """ Gets the components that are not assigned to groups
    """  

    endpoint_url = '/components'
    # create an empty list to add components to
    components = []

    # get all components
    response = make_secure_api_call(base_url+endpoint_url,headers)

    data = response.json()
    for d in data:
        # check if components doesn't have a group
        if d["group"] is None:
            # add component to list
            components.append(d)
    if components == []:
        print("All components are already grouped")
    return components


def get_ungrouped_components_vendors():
    """ Get all vendors that ungrouped components have
    """  
    # get all components without groups
    data = get_comp_no_groups()
    # create empty list to place vendors in
    vendor_list = []

    for d in data:
        for p in d['normalizedProperties']:
            if p['key'] == 'vendor' or p['key'] == 'vendor-name':
                # add vendor to the vendor list
                vendor_list.append(p['value'])
    
    # remove redundancy in the list
    vendor_list = list(dict.fromkeys(vendor_list))
    return vendor_list 
