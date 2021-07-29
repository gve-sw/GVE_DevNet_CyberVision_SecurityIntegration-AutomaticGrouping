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

# GETS THE RESPONSE FROM UMBRELLA, FORMATS IT TO BE READY TO POST

'''
This script gets as the input the response from Umbrella, and formats it to be posted into CV Center

Furthermore, this script is divided into 1 function:
- Funcion 1 (CV_event()):
    DESCRIPTION: stores all the information that is necessary to post on CV into the "payload" dictionary
    INPUTS (1): the output from the Umbrella API
    OUTPUTS (1): the payload/message to be posted
'''

import requests
import json


## FUNCTION
# Formats the output from Umbrella to send to the Cyber Vision Center
def CV_event(umbrella_output):
    # message = "My new, important message"
    message = {}

    # Indicate domain, IP, Date
    message["Domain"] = umbrella_output["domain"]
    message["IP"] = umbrella_output["IP"]
    message["Date"] = umbrella_output["Date"]

    # Store in "message" all the relevant information
    message["Risk Score"] = umbrella_output["url_risk_score"]

    if "url_security_categories" in umbrella_output:
        message["Security Categories"] = umbrella_output["url_security_categories"]
    
    if "url_contentcategories" in umbrella_output:
        message["Content Categories"] = umbrella_output["url_contentcategories"]

    if umbrella_output["url_status"] == 1:
        message["Status"] = "The domain is clean"
    elif umbrella_output["url_status"] == -1:
        message["Status"] = "The domain is malicious"
    elif umbrella_output["url_status"] == 0:
        message["Status"] = "The domain is undefined"

    message["Risk Score"] = umbrella_output["url_risk_score"]

    domain = message["Domain"]
    IP = message["IP"]
    date = message["Date"]
    risk = message["Risk Score"]
    content = message["Content Categories"]
    sec = message["Security Categories"]

    #message = json.dumps(message)
    if "url_security_categories" in umbrella_output and "url_contentcategories" in umbrella_output:
        message = "The domain " + str(domain) + " is malicious and it has been queried by the IP " + str(IP) + " on " + str(date) + ". Its associated risk score is " + str(risk) + "/100. We have found " + str(content) + " as its Content Categories, and " + str(sec) + " as its Security Categories."
    elif "url_security_categories" in umbrella_output:
        message = "The domain " + str(domain) + " is malicious and it has been queried by the IP " + str(IP) + " on " + str(date) + ". Its associated risk score is " + str(risk) + "/100. We have found " + str(sec) + " as its Security Categories."
    elif "url_contentcategories" in umbrella_output:
        message = "The domain " + str(domain) + " is malicious and it has been queried by the IP " + str(IP) + " on " + str(date) + ". Its associated risk score is " + str(risk) + "/100. We have found " + str(content) + " as its Content Categories."
    else:
        message = "The domain " + str(domain) + " is malicious and it has been queried by the IP " + str(IP) + " on " + str(date) + ". Its associated risk score is " + str(risk) + "/100."

    payload = {
    "task": "Malicious DNS Query",
    "alert": {"event-type": "extension_alert", "message": message}
    }

    return payload