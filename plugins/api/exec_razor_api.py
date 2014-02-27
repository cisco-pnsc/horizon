# -*- coding: utf-8 -*-
import json
import requests
import ast
import os

config_path = os.path.abspath(os.path.dirname(__file__)) + '/config.properties'
razor_url = ""

def get_razor_url():
    if razor_url == "":
        config_file = open(config_path, 'r')
        for line in config_file:
            if line.startswith('razor_ipaddress'):
                return 'http://' +  line.replace('razor_ipaddress=','').strip() +':8080/api'
        return ''
    return razor_url

#-- send http get request in order to retrieve database queries
def exec_razor_query(query):
    try:
        r = requests.get(get_razor_url() + query)
   
        return json.loads(r.text)
    except:
        return {}

# -- send http post request in order to execute razor commands such as add item to database, remove item..
def exec_razor_command(command, payload):
    try:
        url = get_razor_url() + "/commands/" + command 
    
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
   
        result = ast.literal_eval(r.text)
       
        if 'error' in result:
            return { "details": result["error"]}
        
        return result
    except:
        try:
            return { "details": "status: %s\ndetails: %s " % (r.status_code,r.text)}
        except:
            return {'details' : 'Failed. Check Razor IP address'}





