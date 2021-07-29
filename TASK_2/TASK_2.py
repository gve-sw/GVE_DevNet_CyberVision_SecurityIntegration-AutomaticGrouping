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

""" Automatically groups the components according to vendor

This script has several components that work together to automatically group components from CyberVision according to vendor.
The helper functions are: 
- create_dictionary: This function is used to create a dictionary to help sort the components
- group_components_by_vendor: This function groups the components by their vendors and adds them into the dictionary
- filter_grouped_components: This function cleans the dictionary by removing the groups with no components

There are then functions that update cybervision with the new grouping:
- update_group: This function updates the groups by adding the components to the group
- create_group: This function creates the new groups (named by vendor) in CyberVision

Lastly, there is the function grouping_algorithm which does the entire process of grouping the components by adding the flow of the functions
"""

import json
import requests
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import env as config 
from helper_functions import make_secure_api_call, get_comp_no_groups, get_ungrouped_components_vendors

base_url = config.CYBERVISION["base_url"]
my_token = config.CYBERVISION["x-token-id"]

headers = {
    "x-token-id" : my_token
}

# HELPER FUNCTIONS

def create_dictionary():
    """ Creates dictionary to be used for sorting
    """
    # create empty dictionary
    grouped_components = {}

    # get a list of all vendors for the ungrouped components
    vendor_names = get_ungrouped_components_vendors()
    for name in vendor_names:
        # add vendors to dictionary as key with empty list as value
        grouped_components[name] = []
    
    # return the dictionary with the added keys
    return grouped_components

def add_component_vendor(vendor_dictionary, component_property, component_id):
    """ Helper function for group_components_by_vendor. Adds component id to dictionary
    
    Parameters
    ----------
    vendor_dictionary: dict
        Dictionary with vendors as keys
    
    component_property: dict
        the property of the component
    
    component_id: str
        id of the component
    """
    if component_property['key'] == 'vendor' or component_property['key'] == 'vendor-name':
        # add component id to the dictionary under the vendor
        vendor_dictionary[component_property['value']].append(component_id)
        #remove redundancy in the component id list
        vendor_dictionary[component_property['value']] = list( dict.fromkeys(vendor_dictionary[component_property['value']]))

def group_components_by_vendor():
    """ Groups components and adds their component id to the dictionary with key according to vendor
    """
    # gets components that are ungrouped
    components = get_comp_no_groups()
    # gets the dictionary with keys that are the vendors but no added components
    grouped_components = create_dictionary()
    
    for component in components:
        component_id = component["id"]
        # go through normalizedProperties of component to find vendors
        for p in component['normalizedProperties']:
            # add component to dictionary under vendor
            add_component_vendor(grouped_components, p, component_id)
    # return the dictionary with keys as vendors and component ids listed under each vendor
    return grouped_components

def filter_grouped_components():
    """ Removes all the keys with empty lists, whether it is by vendor
    """
    # create empty dictionary for the filtered version
    filtered_components = {}
    
    # get dictionary with grouping by vendor
    unfiltered_components = group_components_by_vendor()
    
    for key,value in unfiltered_components.items():
        # only add key,value to filtered dictionary if there are components listed under the key (vendor)
        if value != []:
            filtered_components[key] = value
    
    # Return a dictionary with the components grouped according to vendor 
    return filtered_components 

# UPDATE CYBERVISION FUNCTIONS

def update_group(components, groupId):
    """ Uses API to add component list to group
    
    Parameters
    ----------
    components: list
        list of components to be added
    groupId: str
        id of the group
    """

    headers = {
        "x-token-id" : my_token,
        "Content-Type" : "application/json",
        "Accept" : "application/json"
    }
    endpoint_url = '/groups/' + groupId

    payload = {
        "op": "add",
        "path": "/components",
        "value": components
    }

    try:  
        response = requests.patch(url=base_url+endpoint_url, headers=headers, data=json.dumps(payload), verify=False)
        data = response.json()
    except Exception as e:
        print(response.status_code)
        print(e)

def create_group(label, description, comment):
    """ Uses API to create a new group in CyberVision
    
    Parameters
    ----------
    label: str
        the selected grouping: vendor
    description: str
        description of the created group
    comment: str
        comment to add under the created group
    """    
    endpoint_url = '/groups'
    headers = {
        "x-token-id" : my_token,
        "Content-Type" : "application/json",
        "Accept" : "application/json"
    }
    payload = {
        "color" : "#000000",
        "comments" : comment,
        "criticalness" : 0,
        "description" : description, 
        "label" : label,
        "locked" : False
    }
    response = requests.post(url=base_url+endpoint_url, headers=headers, data=json.dumps(payload), verify=False, allow_redirects=False)
    data = response.json()
    
    return data["id"]

# FINAL FUNCTION TO DO THE AUTOMATED GROUPING
def grouping_algorithm(comment="None"):
    """ Runs the functions together and does the automated grouping by vendor
    
    Parameters
    ----------
    comment: str
        comment to add under the created group
    """    

    # group the components and get the filtered dictionary
    group_dictionary = filter_grouped_components()

    for group, components in group_dictionary.items():
        # create the groups in CyberVision and get the id of the group created
        group_id = create_group(group, "Automated Grouping by vendor", comment)
        # add the components to the group in CyberVision
        update_group(components, group_id)
    
# Example
if __name__ == "__main__":
    print("*****************************************************************************")
    print("Beginning automatic grouping by Vendor name, please wait.")
    print("*****************************************************************************")
    grouping_algorithm("api automatic grouping GVE project")
    print("*****************************************************************************")
    print("Automatic Vendor Grouping complete.")
    print("*****************************************************************************")  
