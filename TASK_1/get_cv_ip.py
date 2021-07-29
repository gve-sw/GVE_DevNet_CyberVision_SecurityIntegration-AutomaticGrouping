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
Collects flows and filters for public IPv4 addresses through a 
rudimentary function.
IPs and their first appearence datetimes are returned as a list of 
dictionaries to be used by a proceeding domain lookup function. 
Lookup is limited by a period defined within env.py. This states the 
range prior to the current date to be filtered. 
- current_t: returns the time and days difference from now until the
    January 1st 1970 starting epoch. This is used as an input to filter 
    the flow get request.
- convert_to_time: converts the millisecond datetime to yyyy/mm/dd 
    hr/min/sec for legibility. 
- isItPublic: returns whether an IP address is IPv4 AND public AND not 
    a reserved IP, exceptions to the rule may have been missed.
- getIps: gathers flows from a defined period, writing the first 
    appearance datetime and IP addresses to a list of dictionaries.
"""

import requests 
import json 
import env as config
from datetime import datetime

# Converts current time to milliseconds to pass within the API calls
def current_t():
    current_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    current_date = datetime.strptime(current_date, "%Y/%m/%d %H:%M:%S")
    epoch = datetime.utcfromtimestamp(0)
    return(current_date - epoch)

# Shortened version of CNs timestamp converter
def convert_to_time(timestamp):
    timestamp = int(str(timestamp)[0:10])
    dt_object = datetime.fromtimestamp(timestamp)
    return str(dt_object)

def isItPublic(stringIp):
    """ 
    Is this IP address public?
    Parameters: string IP address of format "0.0.0.0" - "255.255.255.255"
    If IPv4, public, and not reserved return True, else return False.
    """
    # Private IPs
    if stringIp[0:3] == "10.":
        return False
    for i in range(16, 32):
        check = "172." + str(i) + "."
        if stringIp[0:7] == check:
            return False
    if stringIp[0:8] == "192.168.":
        return False
    # Current networks / Source addresses.
    if stringIp[0] == "0":
        return False
    # Shared address space for SP to subscribers through carrier-grade NAT.
    for i in range(64, 128):
        check = "100." + str(i) + "."
        if i < 100:
            if stringIp[0:7] == check:
                return False
        else:
            if stringIp[0:8] == check:
                return False
    # Loopback addresses to local host.
    if stringIp[0:3] == "127":
        return False
    # Link-local addresses between two hosts on a single link when no 
    # IP address is specified.
    if stringIp[0:7] == "169.254":
        return False
    # IETF protocol assignments.
    if stringIp[0:7] == "192.0.0":
        return False
    # TEST-NET-1 documentation and examples.
    if stringIp[0:7] == "192.0.2":
        return False
    # Reserved 6to4 Relay Anycast.
    if stringIp[0:9] == "192.88.99":
        return False
    # Network Interconnect Device Benchmark Testing.
    for i in range(18, 20):
        check = "198." + str(i) + "."
        if stringIp[0:7] == check:
            return False
    # TEST-NET-2
    if stringIp[0:11] == "198.51.100.":
        return False
    # TEST-NET-3
    if stringIp[0:10] == "203.0.113.":
        return False
    # Reserved for future use.
    for i in range(40, 56):
        check = "2" + str(i) + "."
        if stringIp[0:4] == check:
            return False
    # Broadcast IP.
    if stringIp[0:15] == "255.255.255.255":
        return False
    # Disallow IPv6 as the proceeding workflows are not compatible.
    for p in stringIp:
        if p == ":":
            return False
    # The address may be passed to the proceeding function.
    return True

def get_ips():  
    """ 
    Search CV flows and return public IPs and their first appearance .
    1. Gather flows with capacity limited by a period of days, creating 
        a list of IDs.
    2. Loop through the list of flow IDs and pass the IDs into GET 
        requests.
    3. Parse each response and extract the IP address and first activity 
        timestamp of the Left and Right node, the lists are merged, duplicates 
        are avoided.
    4. Convert the timestamp into datetime format, store each IP and 
        firstActivity in a list of dictionaries 
    5. Returned as a list of dictionaries. 
    """

    base_url = config.CYBERVISION["base_url"]
    my_token = config.CYBERVISION["x-token-id"]
    ip_collection = []
    flows_id, ip_list, ip_seen = [], [], []
    days = config.PERIOD['period']
    now = int(current_t().total_seconds()) * 1000

    # Checks that the period to inspect is valid, it must be an integer, 
    # greater than 0, and between the current date and the unix epoch time.
    if not days or not str(days).isdigit() or days < 0 or (now - (days*86400000)) <= 0 or days >= current_t().days:
        print("Please check that the environmental variable 'PERIOD' is an integer greater than 0 but less than " + str(current_t().days)+ ".")
    else:
        
        params = {
            "from" : (now - (days*86400000)),
            "to" : now
        }
        headers = {
            "x-token-id" : my_token
        }
        payload = {}
        endpoint_url = "flows/"

        # Gather Flow IDs, a set period prior from the current date is tested, 
        # this is configured within the environment variables
        response = requests.get(url=base_url+endpoint_url, headers=headers, 
                                params=params, verify=False)
        data = response.json()
        for f in data:
            flows_id.append(f['id'])

        # Access IP's used in Left-Right Flows, filter for Public addressess 
        # only, merge.
        flow_sides = ['left', 'right']
        for a in flows_id:
            response = requests.get(url=base_url+endpoint_url+a, 
                                    headers=headers, params=params, 
                                    verify=False)
            data = response.json()
            for s in flow_sides:
                try:
                    if isItPublic(data[s]['ip']):
                        if not (data[s]['ip'] in ip_list):
                            ip_list.append(data[s]['ip'])
                            ip_seen.append(data['firstActivity'])
                        elif (data[s]['ip'] in ip_list and int(ip_seen[ip_list.index(data[s]['ip'])]) > int(data['firstActivity'])):
                            ip_seen[ip_list.index(data[s]['ip'])] = data['firstActivity']
                except Exception as e:
                    pass 
                    # Catches the exception when no key named 'IP' is found.

        # Convert time after merger, append to IP-time pairs to a list of 
        # dictionaries.
        for n in ip_list:
            ip_collection.append(
                {
                    'ip' : n, 
                    'firstActivity' : convert_to_time(ip_seen[ip_list.index(n)])
                }
            )

        return ip_collection

