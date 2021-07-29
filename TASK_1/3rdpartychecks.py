""" Checks on domain and IP reputation with 3rd party tools

This script runs a domain against 2 different 3rd party tools: WhoisXMLAPI Domain Reputation API and IPQUALITYSCORE IP Reputation Check API.  

This script has two functions, one for each different API call. Both take just a domain in string form and print out the result of the API call in a json file.

There is also a check function to run a domain against both API.
"""

import requests
import json
import env

def make_secure_api_call(url, headers = {}) -> str:
    """ Make API call with error handling

    Parameters
    ----------
    url: str
        The url to make the api call
    headers: dict
        The headers used in the api call
    """
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 429:
            print("You have exceeded the number of API calls allowed for your account")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response

def whoisxml_domain_reputation(domain):
    """ Checks the domain against the WhoisXMLAPI Domain Reputation API and saves the result in a json file
    
    Parameters
    ----------
    domain: str
        The domain you are checking, works with URL and IP address
    
    """
    # Gets API key and Baseurl for API call from env.py file
    apikey = env.WHOISXML.get("apiKey")
    base_url = env.WHOISXML.get("base_url")

    # API call to WhoisXML with domain
    url = f"{base_url}/?apiKey={apikey}&domainName={domain}"
    response = make_secure_api_call(url)

    # Save domain reputation verdict as a json file
    with open(f"whois_{domain}.json", 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)


def ip_quality_score(domain):
    """ Checks the domain against the IPQUALITYSCORE IP Reputation Check API and saves the result in a json file
    
    Parameters
    ----------
    domain: str
        The domain you are checking, works with URL and IP address
    
    """
    # Gets API key and Baseurl for API call from env.py file
    apikey = env.IPQUALITYSCORE.get("apiKey")
    base_url = env.IPQUALITYSCORE.get("base_url")

    # API call to IPQUALITYSCORE with domain
    url = f"{base_url}/{apikey}/{domain}"
    response = make_secure_api_call(url)  

    # Save IP reputation verdict as a json file
    with open(f"ipscore_{domain}.json", 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)


def check(domain):
    """ Checks the domain against both APIs
    
    Parameters
    ----------
    domain: str
        The domain you are checking, works with URL and IP address
    
    """
    # Run domain against both APIs
    whoisxml_domain_reputation(domain)
    ip_quality_score(domain)


testurl = "google.com"
testip = "69.63.181.11" #Facebook IP address
check(testurl)
check(testip)


