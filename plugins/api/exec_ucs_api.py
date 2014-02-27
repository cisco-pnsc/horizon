import requests
import lxml
from lxml import objectify
import ast
import os

config_path = os.path.abspath(os.path.dirname(__file__)) + '/config.properties'
ucs_ipaddress = ""
ucs_username = ""
ucs_password = ""

def get_ucs_parameters():
    if ucs_ipaddress == "" or ucs_username == "" or ucs_password == "":
        params = {}
        config_file = open(config_path, 'r')
        for line in config_file:
            if line.startswith('ucs_ipaddress'):
                params['ucs_ipaddress'] = line.replace('ucs_ipaddress=','').strip()
            if line.startswith('ucs_username'):
                params['ucs_username'] = line.replace('ucs_username=','').strip()
            if line.startswith('ucs_password'):
                params['ucs_password'] = line.replace('ucs_password=','').strip()
        return params
    
    #-- if config params already been set
    return 
    {
     'ucs_ipaddress' : ucs_ipaddress,
     'ucs_username' : ucs_username,
     'ucs_password' : ucs_password
     }
    
    

def call_ucs_command(xml):
    try:
        headers = {'Content-Type': 'application/soap+xml'}
        
        return objectify.fromstring(requests.post('https://'+ get_ucs_parameters()['ucs_ipaddress'] +'/nuova',data=xml, headers=headers, verify = False).text)
    except:
        return {
                 'errorCode' : 'post_err',
                 'errorDescr' :"error in call_ucs_command: can't post request. check ucsm ip address"
        } 
  