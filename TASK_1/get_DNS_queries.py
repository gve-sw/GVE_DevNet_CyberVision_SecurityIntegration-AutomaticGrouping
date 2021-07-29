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

# THIS SCRIPT SIMPLY TAKES THE JSON FILE THAT CONTAINS THE INFORMATION
# ABOUT THE DOMAINS, IPs, AND DATES, AND STORES IT AS A PYTHON
# DICTIONARY

import json

def get_DNS_queries():

    file = open("domains_urls.json", "r")
    domains_list = json.load(file)

    return domains_list