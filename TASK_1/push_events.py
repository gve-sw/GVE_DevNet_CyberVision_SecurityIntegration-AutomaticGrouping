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

# PUSH A GIVEN EVENT INTO CV DASHBOARD

'''
This script gets a payload/report as an input, and uploads it into the CV Center**
** Please note that in order to work, this script should be run locally in the CV Center

This script is divided into 1 function:
- Funcion 1 (push_events()):
    DESCRIPTION: given a report (the message that want to be posted), print the event into the CV Center
    INPUTS (1): report/message/data structure
    OUTPUTS (0): prints the event into CV, and prints the status code from the API request
'''

import requests
import json
from env import *

base_url = CYBERVISION.get("base_url")

## FUNCTION
# Pushes event into the Cyber Vision Center
def push_events(report):
    url = base_url+"extension/test/report" 
    
    response = requests.post(url, json=report)

    print(response.status_code)
