from exec_ucs_api import *



# Checks if an error occurred in xml request
# Note:
# - request failed if response contains a 'status' key
# Return:
# - boolean value
def failed(response):
    return 'errorCode' in response


# Creates a dictionary response which includes error code and description
# Note:
# - status is an error indication
# Return:
# - error dictionary
def get_error(errorCode,errorDescr):
    return {
             'status' :'Failed',
             'errorCode' : errorCode,
             'errorDescr' : errorDescr
            }

# Login to ucs manager:
# Note:
# - open a session in the ucsm
# Required:
# - config file which includes username and password for ucs manager
def login():
    try :
        
        params = get_ucs_parameters()
        
        xml = '<aaaLogin inName="' + params['ucs_username'] +'" inPassword="' + params['ucs_password'] + '"/>'
        
        rsp = call_ucs_command(xml)
        
        return rsp.get('outCookie')
    
    except Exception, e:
        return get_error('login_err', e)

 
# Logout from ucs manager:
# Required:
# - match session login cookie   
def logout(cookie):
    try:
        xml = '<aaaLogout inCookie="' + cookie +'" />'
        
        return call_ucs_command(xml)
        
    except Exception, e:
        return get_error('logout_err', e)


# Query to get all profiles:
# Note:
# - profile known as lsServer with type = instance
# Return:
# - dictionary of all profile short and long names {'dn1':'name1'}
#     e.g {'org-root/org-VOO/ls-VOO2':'VOO2','org-root/org-VOO/ls-VOO10':'VOO10'}
def get_all_profiles():
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="lsServer" cookie="%s" inHierarchical="false">
          <inFilter>
            <eq
            class="lsServer"
            property="type"
            value="instance"/>
            </inFilter>    
        </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        logout(cookie)
        
        all_profiles = {}
        for profile in rsp.outConfigs.lsServer:
            all_profiles[profile.get('dn')] = profile.get('name') 
        
        return all_profiles 
    except:
        return {} 


# Query to get all macs:
# Note:
# - mac known as adaptorHostEthIf
# Return:
# - dictionary of all macs  {'mac_dn' : 'mac_address'}
def get_all_macs():
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="adaptorHostEthIf" cookie="%s" inHierarchical="false">
                <inFilter/>
                </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        logout(cookie)
        
        all_macs = {}
        for mac in rsp.outConfigs.adaptorHostEthIf:
            # set mac to be the first vnic mac address 
            if (mac.get('id') == '1'):
                all_macs[mac.get('dn')] =  mac.get('mac') 
        
        return all_macs 
    except:
        return {}  


# Return mac address for a server from a list of mac addresses
# Required:
# - server : server id
# - macs : list of all macs
# Return:
# - mac address for server
def get_server_mac(server, macs):
    mac = [mac_addr for mac_dn,mac_addr in macs.items() if server in mac_dn]
    mac = '' if mac == [] else mac[0]
    return mac


# Return the name of the profile which associated to the server 
# Required:
# - name : full name of profile org-root/org-org/ls-VOO2
# Return:
# - if profile hound return profile name : partial name - VOO2 otherwise return ''
def get_server_name(name,profiles):
    if name in profiles:
        return profiles[name]
    return '-'*4

# Query to get all servers:
# Notes:
# - computeBlade is the classId for servers 
# Return:
# - dictionary with all servers information e.g {'server_id': { full info... } }
def get_all_servers():
    
    try:
        
        all_profiles = get_all_profiles()
        all_macs = get_all_macs()
        cookie = login()
        
        xml = '''<configResolveClass classId="computeBlade" cookie="%s" inHierarchical="true">
              <inFilter/>
              </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        
        logout(cookie)
    
        servers = {}
        for server in rsp.outConfigs.computeBlade:
            associated = True if server.get('assignedToDn') != '' else False

            server = {
                        'name' : get_server_name(server.get('assignedToDn'), all_profiles),
                        'id' : server.get('dn').replace('/',':'),
                        'chassis_id' : server.get('chassisId'),
                        'slot_id' : server.get('slotId'),
                        'ip_address' : server.mgmtController.vnicIpV4PooledAddr.get('addr'),
                        'mac' : get_server_mac(server.get('dn'), all_macs),
                        'cpu' : server.get('numOfCpus'),
                        'ram' : server.get('totalMemory'),    # ==> check if it should be 'availableMemory'
                        'associate' : associated,
                        'on' : server.get('operPower'),
                        'fsm': server.get('fsmProgr') + '%'
                    }
            servers[server['id']] = server
        
        return servers
    except:
        return {}

# Query to get all available servers:
# Notes:
# - computeBlade is the classId for servers 
# - association = none for all available servers 
def get_all_available_servers():
    
    try:
        all_profiles = get_all_profiles()
        all_macs = get_all_macs()
        cookie = login()
        
        xml = '''<configResolveClass classId="computeBlade" cookie="%s" inHierarchical="true">
              <inFilter>
              <eq class="computeBlade" property="association" value="none"/>
              </inFilter>
              </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        
        logout(cookie)
        
        available_servers = {}
        for server in rsp.outConfigs.computeBlade:
            server = {
                        'name' : get_server_name(server.get('assignedToDn'), all_profiles),
                        'id' : server.get('dn').replace('/',':'),
                        'chassis_id' : server.get('chassisId'),
                        'slot_id' : server.get('slotId'),
                        'mac' : get_server_mac(server.get('dn'), all_macs),
                        'ip_address' : server.mgmtController.vnicIpV4PooledAddr.get('addr'),
                        'cpu' : server.get('numOfCpus'),
                        'ram' : server.get('totalMemory'),    # ==> check if it should be 'availableMemory'
                        'associate' : False,
                        'on' : server.get('operPower'),
                        'fsm': server.get('fsmProgr') + '%'
                    }
            available_servers[server['id']] = server     
        
        return available_servers
    except:
        return {}
    
# Query to get all unavailable servers:
# Notes:
# - computeBlade is the classId for servers 
# - association = associated for all unavailable servers            
def get_all_unavailable_servers():
    
    try:
        all_profiles = get_all_profiles()
        all_macs = get_all_macs()
        cookie = login()
        
        xml = '''<configResolveClass classId="computeBlade" cookie="%s" inHierarchical="true">
        <inFilter>
        <eq class="computeBlade" property="association" value="associated"/>
        </inFilter>
        </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        logout(cookie)
        
        available_servers = {}
        for server in rsp.outConfigs.computeBlade:
            server = {
                        'name' : get_server_name(server.get('assignedToDn'), all_profiles),
                        'id' : server.get('dn').replace('/',':'),
                        'chassis_id' : server.get('chassisId'),
                        'slot_id' : server.get('slotId'),
                        'mac' : get_server_mac(server.get('dn'), all_macs),
                        'ip_address' : server.mgmtController.vnicIpV4PooledAddr.get('addr'),
                        'cpu' : server.get('numOfCpus'),
                        'ram' : server.get('totalMemory'),    # ==> check if it should be 'availableMemory'
                        'associate' : True,
                        'on' : server.get('operPower'),
                        'fsm': server.get('fsmProgr') + '%'
                    }
            available_servers[server['id']] = server
                       
        return available_servers
    except:
        return {}
               
# query to get server details:
# Required:
# - server dn e.g sys:chassis-2:blade-4
# Note:
# - there are ':' instead of '/' in order to not harm the url address in the HTTP Get request 
#    in the forms.py module
# Return:
# - dictionary with all server info
def get_server_details(server_id):
    
    try:
        all_profiles = get_all_profiles()
        
        cookie = login()
        
        xml = '''<configResolveClass classId="computeBlade" cookie="%s" inHierarchical="true">
            <inFilter>
              <eq class="computeBlade" property="dn" value="%s"/>
            </inFilter>
        </configResolveClass>''' % (cookie,server_id.replace(":","/"))
        
        rsp = call_ucs_command(xml)

        logout(cookie)       
        
        if not hasattr(rsp.outConfigs,'computeBlade'):
            # blade not found
            return get_error('--', 'Blade not found')
        
        rsp = rsp.outConfigs.computeBlade      
        
        associated = False if rsp.get('assignedToDn') == '' else True
        
        if hasattr( rsp.adaptorUnit,'adaptorHostEthIf'):
            mac= [i.get('mac') for i in rsp.adaptorUnit.adaptorHostEthIf if i.get('id') == '1']
            mac = 'none' if mac == [] else mac[0]
        else:
            mac = 'none'

        #return all server details
        return {'name':get_server_name(rsp.get('assignedToDn'), all_profiles),
                'id' : rsp.get('dn').replace('/',':'),
                'assignedToDn' : rsp.get('assignedToDn'),
                'associate' : associated,
                'chassis_id' : rsp.get('chassisId'),
                'slot_id' : rsp.get('slotId'),
                # -- inventory : motherboard
                'cpu_model' : rsp.computeBoard.processorUnit.get('model'),
                'cpu':rsp.get('numOfCpus'),
                'cores' : rsp.computeBoard.processorUnit.get('cores'),
                # -- inventory : CIMC
                'mac' : mac,
                'ip_address' : rsp.mgmtController.vnicIpV4PooledAddr.get('addr'),
                'subnet_mask' : rsp.mgmtController.vnicIpV4PooledAddr.get('subnet'),
                'default_gw' : rsp.mgmtController.vnicIpV4PooledAddr.get('defGw'),
                # -- inventory : memory
                'ram': rsp.get('totalMemory'),
                # -- firmware: Bios
                'bios_model' : rsp.biosUnit.get('model'),
                'bios_running_version' :  rsp.biosUnit.firmwareRunning.get('version'),
                'bios_setup_version' : rsp.biosUnit.firmwareBootDefinition.firmwareBootUnit.get('version'),
                'bios_backup_version' : rsp.biosUnit.firmwareUpdatable.get('version'),
                # -- firmware: BoardController
                'bc_model' : rsp.computeBoardController.mgmtController.get('model'),
                'bc_running_version' :  rsp.computeBoardController.mgmtController.firmwareRunning.get('version'),
                'bc_setup_version' : rsp.computeBoardController.mgmtController.firmwareBootDefinition.firmwareBootUnit.get('version'),
                 # -- firmware: CIMC controller
                'cimc_model' : rsp.mgmtController.get('model'),
                'cimc_running_version' :  rsp.mgmtController.firmwareRunning.get('version'),
                'cimc_setup_version' : rsp.mgmtController.firmwareBootDefinition.firmwareBootUnit.get('version'),
                'cimc_backup_version' : rsp.mgmtController.firmwareUpdatable.get('version'),
                # -- general info
                'on' : rsp.get('operPower'),
                'fsm': rsp.get('fsmProgr')  + '%'
        }
        
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))


print get_server_details('sys:chassis-2:blade-20')

# Query to get all organizations:
# Note:
# - organization is known as orgOrg
# Return:
# - list of all organizations names -- for now: not full name
def get_all_organizations():
    try:
        cookie = login()
        
        xml = '''
        <orgResolveElements
        dn="org-root"
        inClass="orgOrg"
        inSingleLevel="false"
        cookie="%s" inHierarchical="false">
        <inFilter/>
        </orgResolveElements>''' % cookie
        
        rsp = call_ucs_command(xml)
        logout(cookie)
        
        return [org.orgOrg.get('name') for org in rsp.outConfigs.pair]
    except:
        return {}

# query to get all templates:
# Note:
# - template is known as lsServer with type != instance
# Return:
# - list of all templates names
def get_all_templates():
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="lsServer" cookie="%s" inHierarchical="false">
          <inFilter>
            <ne
            class="lsServer"
            property="type"
            value="instance"/>
            </inFilter>    
        </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        logout(cookie)

        all_templates = {}
        for template in rsp.outConfigs.lsServer:
            all_templates[template.get('dn')] = {
                                   'id' : template.get('dn').replace('/',':'),
                                   'name' : template.get('name'),
                                   'type' : template.get('type')
                                   }
        return all_templates 
    except:
        return {}


# Query to get template dn:
# Required:
# - template name e.g OpenStack
# Note:
# - template is known as lsServer with type != instance
# Return:
# - template dn. Full path for template /org-root/ls-OpenStack
def get_template_dn(template_name):
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="lsServer" cookie="%s" inHierarchical="false">
                    <inFilter>
                    <ne
                    class="lsServer"
                    property="type"
                    value="instance"/>
                    <eq
                    class="lsServer"
                    property="name"
                    value="%s"/>
                    </inFilter>        
                    </configResolveClass>
                ''' % (cookie,template_name)
                
        rsp = call_ucs_command(xml)
        
        logout(cookie)             
        
        return rsp.outConfigs.lsServer.get('dn')
    except:
        return ''

# Query to get profile dn:
# Required:
# - profile name e.g python_from_ui0
# Note:
# - profile known as lsServer with type = instance
# Return:
# - profile dn. Full path for profile org-root/org-plugin/ls-python_from_ui0
def get_profile_dn(profile_name):
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="lsServer" cookie="%s" inHierarchical="false">
                    <inFilter>
                    <eq
                    class="lsServer"
                    property="type"
                    value="instance"/>
                    <wcard
                    class="lsServer"
                    property="name"
                    value="%s[0-9]*"/>
                    </inFilter>        
                    </configResolveClass>
                ''' % (cookie,profile_name)
                    
        rsp = call_ucs_command(xml)
        
        logout(cookie)   
        
        return rsp.outConfigs.lsServer.get('dn')
    except:
        return ''
    
# Query to get org full path:
# Required:
# - org name e.g plugin
# Note:
# - org known as orgOrg
# Return:
# - org dn. Full path for org /org-root/org-plugin
def get_org_full_path(org_name):
     try:
        cookie = login()
        
        xml = '''
        <orgResolveElements
        dn="org-root"
        inClass="orgOrg"
        inSingleLevel="false"
        cookie="%s" inHierarchical="false">
        <inFilter>
        <eq 
            class = "orgOrg"
            property="name"
            value ="%s" />
        </inFilter>
        </orgResolveElements>''' % (cookie,org_name)
        
        rsp = call_ucs_command(xml)
        
        logout(cookie)           
        
        return rsp.outConfigs.pair.orgOrg.get('dn')
     except:
        return ''
    
# Creates x copies of profile from template
# Required:
# - template name e.g OpenStack
# - target organization name e.g plugin
# - prefix_name of profile
# - number to start count from
# - number of copies
# Note:
# - create a profile known as lsInstantiateNNamedTemplate
# Return:
# - the post response contains list of all new initialized profiles 
# if fails - return False 
def create_profile_from_template(template_name,prefix_name,target_org,start_num, copies):
    try:
        profiles_per_copies = ''.join(['<dn value="%s%d"/>' % (prefix_name,i) for i in range(start_num,start_num+copies)])
        
        template_dn = get_template_dn(template_name)
        target_org_dn = get_org_full_path(target_org)    

        if template_dn == '' or  target_org_dn == '':
            return get_error('create_template_err','create_profile_from_template : error in template or target organization name')
         
        cookie = login()
        
        xml = '''<lsInstantiateNNamedTemplate
                dn="%s"
                inTargetOrg="%s"
                inHierarchical="false"
                 cookie="%s" inErrorOnExisting="true">
                    <inNameSet>
                        %s
                    </inNameSet>
                </lsInstantiateNNamedTemplate>''' % (template_dn, target_org_dn ,cookie, profiles_per_copies)
        
        rsp = call_ucs_command(xml)
       
        logout(cookie)             
        
        if failed(rsp):
            raise Exception('error')
        
        return rsp 
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))
    
# Associates profile to server
# Required:
# - full profile name e.g org-root/org-plugin/ls-$PROFILE_NAME$
# - server name
# Note:
# - needs a profile. not a template!
# Return:
# - post response 
def associate_profile_to_server(profile,server):
    try:
        cookie = login()
        
        xml = '''<configConfMos
                cookie="%s" inHierarchical="false">
              <inConfigs>
                <pair key="%s/pn">
                    <lsBinding
                        dn="%s/pn"
                        pnDn="%s"
                        restrictMigration="no">
                    </lsBinding>
                </pair>
              </inConfigs>
            </configConfMos>''' % (cookie, profile, profile, server.replace(':','/'))
    
        rsp = call_ucs_command(xml)

        logout(cookie)             

        if failed(rsp):
            raise Exception('error')
        
        return rsp 
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Associates profile to server from template
# Required:
# - template name e.g OpenStack1
# - profile_prefix :  prefix for the profiles that are been created
# - target_org : name of the organization the profile will be related to
# - server: server id
# Note:
# - creates a profile from template and associate it to server
# Return:
# - response. if failed - return error 
def associate_service_profile_from_template(template,profile_prefix,target_org,server):
    try:
        
        rsp = create_profile_from_template(template,profile_prefix,target_org ,0 , 1)
        
        profile_full_name = rsp.outConfigs.lsServer.get('dn')
        
        rsp = associate_profile_to_server(profile_full_name,server)
        
        if failed(rsp):
            raise Exception('error')
        
        return rsp 
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))
        
# Returns only dissociate servers
# Required:
# - list of all servers names 
# Note:
# - in order to prevent a duplicate assignment to the same server
# Return:
# - List of dissociate servers only

def get_dissociate_servers(servers):        
     return [server for server in servers if server in get_all_available_servers()]
 

# Associates a single profile to multiple servers
# Required:
# - template name e.g OpenStack1
# - list of servers
# Note:
# - duplicate profile according to servers list length
# Return: list of all new assoicated blades
def associate_multiple_service_profiles_from_template(template,profile_prefix, target_org, start_num,servers):  
    try:
        
        # extract only dissociate servers
        servers = get_dissociate_servers(servers)
        
        if not len(servers):
            return get_error('associate_multiple_error','Unable to assign profile. No server have been selected. Choose only dissociate servers.' )        
       
        rsp = create_profile_from_template(template, profile_prefix, target_org, start_num, len(servers))
        
        new_associated_blades = {}
        i = 0 
        for profile in rsp.outConfigs.lsServer :
            profile_full_name = profile.get('dn')
        
            result = associate_profile_to_server(profile_full_name,servers[i])
            
            if failed(result):
                return result
            
            new_associated_blades[servers[i]]= profile_full_name 
            i += 1
    
        return new_associated_blades
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Dissociates a profile from a template
# Required:
# - profile full name e.g org-root/OpenStack01
# Return:
# - True if dissociation was successful, otherwise- False
def disassociate_service_profile(profile_dn):
    try:
        
        cookie = login()

        xml = '''<configConfMos
             cookie="%s" inHierarchical="false">
            <inConfigs>
            <pair
            key="%s/pn">
            <lsBinding
            dn="%s/pn"
            status="deleted">
            </lsBinding>
            </pair>
            </inConfigs>
            </configConfMos>''' % (cookie, profile_dn, profile_dn)

        rsp = call_ucs_command(xml)
        
        logout(cookie)             
       
        return rsp.outConfigs.pair.lsBinding.get('status') == 'deleted'
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Deletes profile from ucsm
# Required:
# - full profile name e.g org-root/OpenStack01
# Return:
# - response if deletion was successful. otherwise- False.
def delete_profile(profile_dn):
    try:
        
        cookie = login()
            
        xml = '''<configConfMos
             cookie="%s" inHierarchical="false">
            <inConfigs>
            <pair
            key="%s">
            <lsServer
            dn="%s"
            status="deleted">
            </lsServer>
            </pair>
            </inConfigs>
            </configConfMos>''' % (cookie, profile_dn, profile_dn)

        rsp = call_ucs_command(xml)
        
        logout(cookie)             
       
        return rsp.outConfigs.pair.lsServer
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Dissociates profile to server
# Required:
# - server id e.g sys/chassis-2/blade-5
# Note:
# - unassign profile to server includes 2 steps:
#    1. dissociate profile from a template
#    2. delete profile
# Return:
# - response if unassign succeed otherwise- False.
def disassociate_service_pofile_to_server(server_id):
    try:
        
        server_details = get_server_details(server_id)

        if failed(server_details):
            return get_error(server_details['errorCode'] ,server_details['errorDescr'])
        
        profile_associate = server_details['assignedToDn']
        
        if profile_associate == '':
            return {}
        
        rsp = disassociate_service_profile(profile_associate)
        
        #---- check if needed?
        rsp = delete_profile(profile_associate)
       
        return rsp
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# action: shutdown server
# Required:
# - server id e.g sys/chassis-2/blade-5
# - is_hard : boolean field to determine how to shutdown the server
#              if True, a hard shutdown will be performed, otherwise a soft one.
# Return:
# - response if shutdown succeed otherwise- False.    
def shutdown_server(server_id, is_hard):
    try:
        
        server_details = get_server_details(server_id.replace(':','/'))
        
        state = 'admin-down' if is_hard else 'soft-shut-down'
        
        # if an error occur while retrieving server details exit function
        if failed(server_details):
            return get_error(server_details['errorCode'] ,server_details['errorDescr'])
           
        profile_full_name = server_details['assignedToDn']
        
        cookie = login()
        xml = '''<configConfMo dn="%s/power" cookie="%s" inHierarchical="false">
            <inConfig>
            <lsPower dn="%s/power" state="%s"></lsPower>
            </inConfig>
            </configConfMo>''' % (profile_full_name,cookie,profile_full_name, state)
        
        rsp = call_ucs_command(xml) 
        logout(cookie)
        return rsp
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Boots server 
# Required:
# - server id e.g sys/chassis-2/blade-5
# Return:
# - response if power on succeed otherwise- False.     
def boot_server(server_id):
    try:
        
        server_details = get_server_details(server_id.replace(':','/'))
        
        # if an error occur while retrieving server details exit function
        if failed(server_details):
            return get_error(server_details['errorCode'] ,server_details['errorDescr'])
        
        profile_full_name = server_details['assignedToDn']
        
        cookie = login()
        xml = '''<configConfMo
                dn="%s/power"
                 cookie="%s" inHierarchical="false">
                <inConfig>
                <lsPower
                dn="%s/power"
                state="admin-up">
                </lsPower>
                </inConfig>
                </configConfMo>''' % (profile_full_name,cookie,profile_full_name)
        
        rsp = call_ucs_command(xml) 
           
        logout(cookie)
        
        if failed(rsp):
            raise Exception('error')
        
        return rsp
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Resets server
# Required:
# - server id e.g sys/chassis-2/blade-5
# Note:
# - restart server includes 2 steps:
#    1. power server off
#    2. power server on
# Return:
# - response if restart succeed otherwise- False. 
def reset_server(server_id):
    try:
        rsp = shutdown_server(server_id, False)
        if failed(rsp):
            raise(Exception('error'))
        
        rsp = boot_server(server_id)
        
        if failed(rsp):
            raise(Exception('error'))
        
        return rsp
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))
        
# Returns server ip in order launch kvm
# Required:
# - server name e.g sys/chassis-2/blade-5
# Return:
# - ip address if succeed. otherwise - return ''
def get_server_ip(server_id):
     try:
         cookie = login()
         xml = '''<configResolveClass classId="ippoolPooled" cookie="%s" inHierarchical="false">
                  <inFilter>
                  <wcard
                    class="ippoolPooled"
                    property="assignedToDn"
                    value="%s.*"/>
              </inFilter> 
            </configResolveClass>''' % (cookie,server_id.replace(':','/'))
        
         rsp = call_ucs_command(xml) 
           
         logout(cookie)
         return rsp.outConfigs.ippoolPooled.get('id')
     except:
         return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# action: get kvm http url 
# Required:
# - server name e.g sys/chassis-2/blade-5
# Return:
# - response if shutdown succeed otherwise- False. 
def get_kvm_url(server_id):

    headers = {'Content-Type': 'text/plain'}
    ip = get_server_ip(server_id)
   
    params = get_ucs_parameters()
    
    data = 'username="%s" password="%s" domain="" cimc_ip="%s"' % (params['ucs_username'], params['ucs_password'], ip)
    return (requests.post('https://' + ip +':44443/ucsm/getkvmurl.cgi',data=data, headers=headers, verify = False).text).replace('outURL:','')


# Returns all multicast policies
# Note:
# - multicast policies known as fabricMulticastPolicy
# Return:
# - list of all multicast policies while creating a new vlan
def get_all_multicast_policies():
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="fabricMulticastPolicy" cookie="%s" inHierarchical="false">
              <inFilter/>
              </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        
        logout(cookie)

        return [mc_policy.get('name') for mc_policy in rsp.outConfigs.fabricMulticastPolicy]
    except:
        return []

# Creates a multicast policy
# Required:
# - mcpolicy_name : multicat policy name
# - icmp_snooping_state
# - icmp_snooping_querier_state
# Note:
# - multicast policies known as fabricMulticastPolicy
# Return:
# - response if creation succeed
def create_multicast_policy(mcpolicy_name, icmp_snooping_state, icmp_snooping_querier_state):
    try:
         cookie = login()
         xml = '''<configConfMos
             cookie="%s" inHierarchical="false">
            <inConfigs>
            <pair
            key="org-root/mc-policy-%s">
            <fabricMulticastPolicy
            descr=""
            dn="org-root/mc-policy-%s"
            name="%s"
            policyOwner="local"
            querierIpAddr="0.0.0.0"
            querierState="%s"
            snoopingState="%s"
            status="created">
            </fabricMulticastPolicy>
            </pair>
            </inConfigs>
            </configConfMos>''' % (cookie,mcpolicy_name, mcpolicy_name , mcpolicy_name, icmp_snooping_querier_state, icmp_snooping_state)
                    
         rsp = call_ucs_command(xml) 
           
         logout(cookie)
         return rsp.outConfigs.pair.fabricMulticastPolicy
    except:
         return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))  

# Deletes multicast policy
# Required:
# - mcpolicy_name : multicat policy name
# Note:
# - multicast policies known as fabricMulticastPolicy
# Return:
# - response if deletion succeed
def delete_multicast_policy(mcpolicy_name):
    try:
         cookie = login()
         xml = '''<configConfMos
             cookie="%s" inHierarchical="false">
            <inConfigs>
            <pair
            key="org-root/mc-policy-%s">
            <fabricMulticastPolicy
            dn="org-root/mc-policy-%s"
            status="deleted">
            </fabricMulticastPolicy>
            </pair>
            </inConfigs>
            </configConfMos>''' % (cookie,mcpolicy_name)
                    
         rsp = call_ucs_command(xml) 
           
         logout(cookie)
         return rsp
    except:
         return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Checks if a multicast policy already exsists
# Required:
# - multicast_policy : multicat policy name
# Note:
# - multicast policies known as fabricMulticastPolicy
# Return:
# - True is exsists otherwise -False.
def is_multicast_policy_exists(multicast_policy):
    try:
        
        if multicast_policy:
            cookie = login()
            
            xml = '''<configResolveClass classId="fabricMulticastPolicy" cookie="%s" inHierarchical="false">
                  <inFilter>
                  <eq class="fabricMulticastPolicy"  property = "name"  value = "%s"/>
                  </inFilter>
                  </configResolveClass>''' % (cookie, multicast_policy)
            
            rsp = call_ucs_command(xml)
            
            logout(cookie)
    
            return rsp.outConfigs.fabricMulticastPolicy
        return {}
    except:
        return get_error('poicy_exists_error' , 'Policy not Found')
             

# Query to get all vlans:
# Notes:
# - fabricVlan is the classId for vlans 
def get_all_vlans():
    
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="fabricVlan" cookie="%s" inHierarchical="false">
              <inFilter/>
              </configResolveClass>''' % cookie
        
        rsp = call_ucs_command(xml)
        
        logout(cookie)
        
        vlans = {}
        for vlan in rsp.outConfigs.fabricVlan:
            if vlan.get('cloud') == 'ethlan':
                native = True if (vlan.get('defaultNet') == 'yes') else False

                vlan = {
                            'id' : vlan.get('dn').replace('/',':'),
                            'name' : vlan.get('name'),
                            'native' : native,
                            'nw_type' : vlan.get('type'),
                            'locale' : vlan.get('locale'),
                            'owner' : vlan.get('policyOwner'),
                            'multicast_policy_name' : vlan.get('mcastPolicyName'),
                            'multicast_policy_instance' : vlan.get('operMcastPolicyName'), 
                            'sharing_type' : vlan.get('sharing'),
                            'fabric_id' : vlan.get('switchId'),
                            'if_type' : vlan.get('ifType'),
                            'transport_type' : vlan.get('transport')
                        }
                vlans[vlan['id']] = vlan
        
        
        return vlans
    except:
        return {}

# Checks if a multicast policy already exsists
# Required:
# - vlan_name : vlan name
# - multicast_policy : multicat policy name
# - conf_arr : array of dictionaries which contains the config information  for each pair [{ 'vlan_id' : 'XXX', 'sharing_type':'none', 'fabric' : 'A' },{ 'vlan_id' : 'YYY', 'sharing_type':'none', 'fabric':'B'}]
# Note:
# - create a new vlan
#Return:
# - response if creation succeed. otherwise return false.
def create_vlan(vlan_name, multicast_policy, conf_arr):
    try:
        
        rsp = is_multicast_policy_exists(multicast_policy)
        # if policy not exists return error. cannot create a vlan without valid policy name 

        if failed(rsp):
            return rsp
           
           
        conf_str = ''
        for conf in conf_arr:
            conf_str += '''
                    <pair
                    key="fabric/lan%s/net-%s">
                    <fabricVlan
                    compressionType="included"
                    defaultNet="no"
                    dn="fabric/lan%s/net-%s"
                    id="%s"
                    mcastPolicyName="%s"
                    name="%s"
                    policyOwner="local"
                    pubNwName=""
                    sharing="%s"
                    status="created">
                    </fabricVlan>
                    </pair>''' % (conf['fabric'], vlan_name,conf['fabric'], vlan_name, conf['vlan_id'], multicast_policy,vlan_name,conf['sharing_type'])
        
        
        cookie = login()
        xml = '''<configConfMos
                 cookie="%s" inHierarchical="false">
                <inConfigs>
                %s
                </inConfigs>
                </configConfMos>''' % (cookie,conf_str)
        
        rsp = call_ucs_command(xml) 
           
        logout(cookie)
        return rsp.outConfigs.pair.fabricVlan
    except:
         return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))

# Deletes a vlan
# Required:
# - vlan_id : vlan name
#Return:
# - response if deletion succeed. otherwise return false.
def delete_vlan(vlan_id):

    try:
         cookie = login()
         xml = '''<configConfMos
                 cookie="%s" inHierarchical="false">
                <inConfigs>
                <pair
                key="%s">
                <fabricVlan
                dn="%s"
                status="deleted">
                </fabricVlan>
                </pair>
                </inConfigs>
                </configConfMos>''' % (cookie,vlan_id.replace(':','/'),vlan_id.replace(':','/'))
                        
         rsp = call_ucs_command(xml) 
           
         logout(cookie)
          # outConfigs is empty. rsp.get('response') = yes.
         return rsp
    except:
         return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))
     
     

# Returns all nic details
# Required:
# - nic_id : nic dn
# Note:
# - nics known as vnicEther
# Return:
# - all required information for a specific nic
def get_nic_details(nic_id):
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="vnicEther" cookie="%s" inHierarchical="true">
          <inFilter>
          <eq
                    class="vnicEther"
                    property="dn"
                    value="%s"/>
          </inFilter>
        </configResolveClass>''' % (cookie, nic_id.replace(':','/'))
        
        rsp = call_ucs_command(xml)
        logout(cookie)
        
        if not hasattr(rsp.outConfigs, 'vnicEther'):
            return get_error('--','Failed to find nic %s' % nic_id)
        
        rsp = rsp.outConfigs.vnicEther
        
        if hasattr(rsp, 'vnicEtherIf'):
            vlans = [vlan.get('name') for vlan in rsp.vnicEtherIf]
            default = [vlan.get('name') for vlan in rsp.vnicEtherIf if vlan.get('defaultNet') == 'yes' ]
            default = 'none' if default == [] else default[0]
        else:
            vlans = []
            default = 'none'
        
        
        nic =  {
               'id' : rsp.get('dn').replace('/',':'),
               'name' : rsp.get('name'),
               'vlans' : vlans,
               'default' : default,
               'adaptorProfileName' : rsp.get('adaptorProfileName'),
               'addr': rsp.get('addr'),
               'adminVcon': rsp.get('adminVcon'),
               'identPoolName' : rsp.get('identPoolName'),
               'mtu': rsp.get('mtu'),
               'nwCtrlPolicyName' : rsp.get('nwCtrlPolicyName'),
               'nwTemplName' : rsp.get('nwTemplName'),
               'order':rsp.get('order'),
               'pinToGroupName' :rsp.get('pinToGroupName'),
               'qosPolicyName' :rsp.get('qosPolicyName'),
               'statsPolicyName' : rsp.get('statsPolicyName'),
               'switchId' : rsp.get('switchId')
               }
    
        return nic 
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr')) 

# Returns all nic vlans
# Required:
# - nic:  a vnicEther object from lxml.objectify (under lsServer)
# Return:
# - list of all related vlans
def get_nic_vlans(nic):
    if hasattr(nic, 'vnicEtherIf'):
        return [vlan.get('name') for vlan in nic.vnicEtherIf]
    return []
  
# Returns all template details
# Required:
# - template_id : template dn
# Note:
# - template known as lsServer
# Return:
# - dictionary with the following information:
#        * template id
#        * template name
#        * all related nics with their vlans
#     e.g: { 'id' : 'template_dn', 'name' : 'template_name', 'nics' : { ['id' : 'nic1_dn', 'name': 'nic1_name' , 'vlans' : ['vlan1','vlan2'..]] , ...}  
def get_template_details(template_id):
    try:
        cookie = login()
        
        xml = '''<configResolveClass classId="lsServer" cookie="%s" inHierarchical="true">
          <inFilter>
          <eq
                    class="lsServer"
                    property="dn"
                    value="%s"/>
          </inFilter>
        </configResolveClass>''' % (cookie, template_id.replace(':','/'))
        
        rsp = call_ucs_command(xml)
        logout(cookie)
        
        
        rsp = rsp.outConfigs.lsServer
        
        return {
                'id' : template_id,
                'name' : rsp.get('name'),
                'nics' : [{
                           'id' : template_id + ':' +nic.get('rn'),
                           'name' : nic.get('name'),
                           'vlans' : get_nic_vlans(nic)
                           } for nic in rsp.vnicEther],
                }
        
    except:
       return {
               'status' : 'Failed',
               'errorCode' : rsp.get('errorCode') ,
               'errorDescr' : rsp.get('errorDescr'),
               'id' : template_id,
               'name' : 'Failed',
               'nics' : []
           }  
  

# Returns a vlan xml string for adding a vlan to a template
# Required:
# - vlan : vlan name
# Note:
# - deletion string includes a status field = 'deleted'
# Return:
# - xml string 
def get_deletion_vnicEtherIf_str(vlan):
    return '''
            <vnicEtherIf
            rn="if-%s"
            status="deleted">
            </vnicEtherIf>''' % vlan

# Note:
# - determine a default vlan includes 'defaultNet'  = 'yes'/'no'
def get_default_vnicEtherIf_str(default, default_net):
   return  '''<vnicEtherIf
                defaultNet="%s"
                rn="if-%s">
                </vnicEtherIf> ''' % (default_net, default)
# Note:
# - creation string includes a name field (not only rn)
def get_creation_vnicEtherIf_str(vlan, default):
    
    default = 'yes' if vlan == default else 'no'
    
    return '''
            <vnicEtherIf
            defaultNet="%s"
            name="%s"
            rn="if-%s">
            </vnicEtherIf>''' % (default,vlan, vlan)


# Returns a vlan xml string for adding a vlan to a template
# Required:
# - old_nic_vlans : list of all old vlans
# - old_default : name of old default vlan
# - new_vlans : list of all new chosen vlans from the ui
# -  new_default : name of new default vlan
# Note:
# - checks for changes in the current state and evalute a suitable string for the xml request
# Return:
# - xml string 
def get_vnicEtherIf_str(old_nic_vlans, old_default , new_vlans, new_default):
    try:
        str = ''
        is_new_default = old_default != new_default
        for old_vlan in old_nic_vlans:
            if not old_vlan in new_vlans:
                str += get_deletion_vnicEtherIf_str(old_vlan)
            else:
                if is_new_default: 
                    if old_vlan == old_default:  
                        str += get_default_vnicEtherIf_str(old_default, 'no')
                    elif old_vlan == new_default:  
                        str += get_default_vnicEtherIf_str(new_default, 'yes')
                new_vlans.remove(old_vlan)
                
        for new_vlan in new_vlans:
            str += get_creation_vnicEtherIf_str(new_vlan,new_default)
        return str
        
    except:
        return ''

# Adds vlan to a template
# Required:
# - nic_id : nic dn
# - vlans : list of all new chosen vlans from the ui
# - default : new default vlan
# Note:
# - modify vlans in a template
# Return:
# - response for additing vlan . if fails return error 
def add_vlan(nic_id,vlans,default):  
    try:
       
       nic = get_nic_details(nic_id)
       
       if failed(nic):
           return get_error(nic['errorCode'], nic['errorDescr'])
       
       vnicEtherIfstr = get_vnicEtherIf_str(nic['vlans'], nic['default'],vlans, default)
       
       nic_id = nic_id.replace(':', '/')
       
       cookie = login()
       
       xml = '''
        <configConfMos
         cookie="%s" inHierarchical="false">
        <inConfigs>
        <pair
        key="%s">
        <vnicEther
        adaptorProfileName="%s"
        addr="%s"
        adminVcon="%s"
        dn="%s"
        identPoolName="%s"
        mtu="%s"
        nwCtrlPolicyName="%s"
        nwTemplName="%s"
        order="%s"
        pinToGroupName="%s"
        qosPolicyName="%s"
        statsPolicyName="%s"
        status="created,modified"
        switchId="%s">%s
        </vnicEther>
        </pair>
        </inConfigs>
        </configConfMos>''' % (cookie, nic_id, nic['adaptorProfileName'], nic['addr'],nic['adminVcon'],nic_id, nic['identPoolName'],
                             nic['mtu'], nic['nwCtrlPolicyName'], nic['nwTemplName'], nic['order'], nic['pinToGroupName'],
                             nic['qosPolicyName'],nic['statsPolicyName'], nic['switchId'],vnicEtherIfstr)


       rsp = call_ucs_command(xml)
       logout(cookie)

       return rsp.outConfigs.pair.get('key')
    except:
        return get_error(rsp.get('errorCode'),rsp.get('errorDescr'))   


# for 'download summary' button - helps to initiate script (for now it's a cvs file)        
# returns a dictionary with all servers info
# e.g : {'sys:chassis-2:blade-5': {'id': 'sys:chassis-2:blade-5','name':'VOO2', 'mac': 'FF:FF:FF:FF:FF:FF' ....}}
def get_context_data(servers):
    all_servers = get_all_servers()
    context = {}
    for server in servers:
        if server in all_servers:
            context[server] = all_servers[server]

    return context