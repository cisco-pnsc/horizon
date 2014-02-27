from exec_razor_api import *


# ----- General ------
def get_collection(type):
    query = '/collections/%s' % type
    all = {}
    
    for item in exec_razor_query(query):
        all[item['name']] = exec_razor_query(query + '/' + item['name'])
    
    return all

# ----- Nodes --------
def get_all_nodes():
    print("razor server :---> get_all_nodes")

    all_nodes = get_collection('nodes')
   
    for node, node_details in all_nodes.items():
        node_details["status"] = get_node_status(node)
        try:
            node_details["ipaddress"] = node_details["facts"]["ipaddress"]
        except:
            node_details["ipaddress"] = "Not bound to a policy yet"

    return all_nodes

print get_collection('nodes')


def get_node_log(node_name):
    return exec_razor_query('/collections/nodes/' + node_name + '/log')

def get_status(log_line, is_rebind):
    if "event" in log_line: 
        status = log_line["event"]
        if status == "boot":
            return "Boot"
        elif status == "stage_done":
            return "Broker"
        elif status == "bind" and not(is_rebind): 
            return "Bind"
        elif status == "bind" and is_rebind: 
            return "Broker"
        elif status == "unbind": 
            return "Unbound"
        else:
            return "Installer"
    else:
        return ""
        
def get_node_status(node_name):
       
    data = get_node_log(node_name)

    if "error" in data :
        return "No Status Was Found"
   
    status = ""
    is_rebind = False
    
    for log_line in data:
        if get_status(log_line, is_rebind) != "":
            status = get_status(log_line, is_rebind)
            if status == "Broker":
                is_rebind = True

    if status != "":
     return status

    return "Error Occurred While Retrieving Status"


def get_node_details(node_name):
    data = exec_razor_query('/collections/nodes/' + node_name)

    if data != {}:
	if 'facts' in data:
		ipaddress = data["facts"]["ipaddress"]
	else: 
		ipaddress = "Not bound to a policy"    
    	try:
            return { 
             "id" :node_name,
             "name" : node_name,
             "spec" : data["id"],
             "status" :  get_node_status(node_name),
             "ipaddress" : ipaddress,
             "log_link" : data["log"]["id"],
             "policy" : data["policy"]["name"],
             "tags" : [tag["name"] for tag in data["tags"]],
             "all_info" : str(data) 
            }
        except:
            return { 
             "id" :node_name,
             "name" : node_name,
             "spec" : data["id"],
             "status" :  get_node_status(node_name),
             "ipaddress" : ipaddress,
             "log_link" : '',
             "policy" : 'Not bound to a policy',
             "tags" : "",
            }
	else:
	     return { 
             "id" :node_name,
             "name" : node_name,
             "details" : 'Failed Retreiving Node Details. Node is Unbound'
            }

def delete_node(node_name):
    print("razor server :---> delete_node")
   
    node = { "name" : node_name}
    
    details = exec_razor_command("delete-node", node)
    
    try:
        return  {
                "node_name" : node_name,
                "details" : details["details"]
            }
    except: 
        return  {
                "node_name" : node_name,
                "details" : ""
            }

def unbind_node(node_name):
    print("razor server :---> unbind_node")
    node = { "name" : node_name}
    
    details = exec_razor_command("unbind-node", node)
    
    if "result" in details :
        details["details"] = details["result"]
    try:
        return  {
                "node_name" : node_name,
                "details" : details["details"]
            }
    except: 
        return  {
                "node_name" : node_name,
                "details" : ""
            }


# ----- Repositories --------
def get_all_repos():
    print("razor server :---> entered get_all_repos")

    return get_collection('repos')

def create_repo(repo_name, iso_url):
    print("razor server :---> entered create_repo")
   
    repo = {
             "name": repo_name,
             "iso-url": iso_url
        }
    
    details = exec_razor_command("create-repo", repo)
        
    try:
        return  {
                "name" : repo["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : repo["name"],
                "details" : ""
            }

def delete_repo(repo_name):
    print("razor server :---> delete_repo")
    
    repo = {"name": repo_name}
    
    details = exec_razor_command("delete-repo", repo)
    try:
        return  {
                "name" : repo["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : repo["name"],
                "details" : ""
            }

# ----- Brokers --------
def create_broker(broker):
    print("razor server :---> entered create_broker")
    
    #--- doing so because table fields should be also attribute in broker model
    configuration = {}
    if broker.configuration_server:
    	configuration["server"] = broker.configuration_server
    if broker.configuration_version:
    	configuration["version"] = broker.configuration_version

    broker = {
              "name": broker.name,
              "configuration": configuration,
              "broker-type": broker.broker_type
            }
    details = exec_razor_command("create-broker", broker)
    try:
        return  {
                "name" : broker["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : broker["name"],
                "details" : ""
            }
    
def get_all_brokers():
    print("razor server :---> entered get_all_brokers")
    
    return get_collection('brokers')

# ----- Tags --------
def create_tag(tag):
    print("razor server :---> entered create_tag")

    tag = {'name': tag.name,
            'rule' : ast.literal_eval(tag.rule) }
    
    details = exec_razor_command("create-tag", tag)
    try:
        return  {
                "name" : tag["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : tag["name"],
                "details" : ""
            }


def delete_tag(tag_name):
    print("razor server :---> delete_tag")
    
    tag = { "name" : tag_name}
    
    details = exec_razor_command("delete-tag", tag)
    try:
        return  {
                "name" : tag_name,
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : tag_name,
                "details" : ""
            }

def get_tag_details(tag_name):
    print("razor server :---> get_tag_details")
     
    data = exec_razor_query('/collections/tags/' + tag_name)
    
    try:
        return {
                "name" : data["name"],
                "rule" : data["rule"],
                "details" : ""
            }
    except:
        return {
                "name" : tag_name,
                "details" : data
            }

def update_tag(tag):
    print("razor server :---> update_tag")
        
    tag.rule = tag.rule

    tag = {'name': tag.name,
            'rule' : ast.literal_eval(tag.rule) } 
    
    data = exec_razor_command("update-tag-rule", tag)
    try:
        return  {
                "name" : tag["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : tag["name"],
                "details" : ""
            }
    
def get_all_tags():
    print("razor server :---> entered get_all_tags")
    
    return get_collection('tags')

# ----- Installers --------
def create_installer(installer):
    print("razor server :---> entered create_installer")
    
    installer = {
                  "name": installer.name,
                  "os": installer.os,
                  "os_version": installer.os_version,
                  "description": installer.description,
                  "boot_seq": installer.boot_seq.copy(),
                  "templates": installer.templates.copy()
                }
      
    details = exec_razor_command("create-installer", installer)
    
    try:
        return  {
                "name" : installer["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : installer["name"],
                "details" : ""
            }


# ----- Policies --------
def create_policy(policy):
    print("razor server :---> entered create_policy")
    tags_arr = []
    
    for tag in ast.literal_eval(policy.tags):
        try:
            tags_arr.append({"name" : tag["name"] , "rule" : ast.literal_eval(tag["rule"])})
        except: 
            tags_arr.append({"name" : tag["name"]})
 
            
    policy = {
                  "name": policy.name,
                  "repo": {'name': policy.repo},
                  "installer": {'name' : policy.installer},
                  "broker": {'name' : policy.broker },
                  "hostname": policy.hostname,
                  "root_password": policy.root_password,
                  "max_count": policy.max_count,
                  "rule_number": policy.rule_number,
                  "tags": tags_arr,
                  "enabled" : policy.enabled
              }
    
    details = exec_razor_command("create-policy", policy)
    try:
        return  {
                "name" : policy["name"],
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : policy["name"],
                "details" : ""
            }
  
def enable_policy(policy_name):
    print("razor server :---> enable_policy")

    policy  =  { "name" : policy_name}
    details = exec_razor_command("enable-policy", policy)
    
    try:
        return  {
                "name" : policy_name,
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : policy_name,
                "details" : ""
            }

def disable_policy(policy_name):
    print("razor server :---> disable_policy")
    
    policy  =  { "name" : policy_name}
    
    details = exec_razor_command("disable-policy", policy)
    
    try:
        return  {
                "name" : policy_name,
                "details" : details["details"]
            }
    except: 
        return  {
                "name" : policy_name,
                "details" : ""
            }

def is_policy_enable(policy_name):
    print("razor server :---> is_policy_enable")
   
    is_enabled = get_policy_details(policy_name)["enabled"]

    return { "enabled" : is_enabled} 

def get_policy_details(policy_name):
    print("razor server :---> get_policy_details")
     
    data = get_razor_collection("policies/" + policy_name)
    
    try:
        return {
                  "name": data["name"],
                  "repo": data["repo"]["name"],
                  "installer": data["installer"]["name"],
                  "broker": data["broker"]["name"],
                  "hostname": data["configuration"]["hostname_pattern"],
                  "root_password": data["configuration"]["root_password"],
                  "max_count": data["max_count"],
                  "rule_number": data["rule_number"],
                  "tags": data["tags"],
                  "enabled" : data["enabled"],
                  "all_info" : str(data),
                  "details" : ""
                }
    except:
        return {
                   "name": data["name"],
                   "details" : str(data)
                }
        
def get_all_policies():
    print("razor server :---> entered get_all_policies")

    return get_collection("policies")



