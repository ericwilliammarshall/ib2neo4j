#! /usr/bin/env python3

import os
import re

hostTxtFile = 'ibhosts.txt'	
#linkFile = 'iblinkinfo.txt'
linkTxtFile = 'test.txt'
switchTxtFile = 'ibswitches.txt'

# links' key is the 'near' gid
# near gid --> connection --> far gid
LINKS = {}
HOSTS = {}
SWITCHES = {}


def process_switch_file( switchFile ):
    with open(switchFile) as switchFileHandle:
        switchRegexPattern = re.compile ( r'\w+\s+: (\w+) ports (\d+) \"(.*)\" .*') 
        for line in switchFileHandle:
            # find the switch id
    
            # example input:
            # Switch	: 0xec0d9a030002b810 ports 37 "SwitchIB Mellanox Technologies" base port 0 lid 496 lmc 0
            # Switch	: 0xec0d9a0300e05f80 ports 37 "MF0;switch-9625d4:MSB7800/U1" enhanced port 0 lid 566 lmc 0
            # Switch	: 0xec0d9a030002b810 ports 37 "MF0;switch-9625d4:MSB7800/U1" enhanced port 0 lid 566 lmc 0
            #switchRegex = re.match ( r'\w+\s+: (\w+) ports (\d+) \"(.*)\" .*', line ) 
            switchRegex = switchRegexPattern.match ( line ) 
            gid  =  switchRegex.group(1) 
            ports = switchRegex.group(2) 
            name =  switchRegex.group(3) 
            SWITCHES[gid] = {
                    'name': name, 
                    'ports': ports,
                    }
            #print(gid, name, ports)
        
def process_host_file( hostFile ):
    hostRegexPattern = re.compile ( r'\w+\s+: (\w+) ports (\d+) \"(.*)\"' ) 
    with open(hostFile) as hostFileHandle:
        for line in hostFileHandle:
            #print(line)
            # example input:
            #Ca	: 0xec0d9a03006ed0ca ports 1 "quorum01 HCA-2"
            #hostRegex = re.match ( r'\w+\s+: (\w+) ports (\d+) \"(.*)\"', line ) 
            hostRegex = hostRegexPattern.match ( line ) 
            gid  =  hostRegex.group(1) 
            ports = hostRegex.group(2) 
            name =  hostRegex.group(3) 
            HOSTS[gid] = {
                    'name': name, 
                    'ports': ports,
                    }
            #print(gid, name, ports)
    
def process_links_file( linkFile ):
    linkRegexNearPattern =  re.compile ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)') 
    linkRegexConnectionPattern =  re.compile ( r'\( (\w\w)\s+(\d+.\d+ \w+) (\w+)/\s+(\w+)\)') 
    linkRegexFarPattern =  re.compile ( r'>\s+(\w+)\s+(\d+)\s+(\d+).*\"(.*)\.*"') 
    with open(linkFile) as linkFileHandle:
        for line in linkFileHandle:
            # example input:
            # 0x248a07030017b128 "                  thing4 HCA-1"    612    1[  ] ==( 4X      25.78125 Gbps Active/  LinkUp)==>  0xec0d9a030002b810    496   20[  ] "SwitchIB Mellanox Technologies" ( )
            # 0xec0d9a03006ed0ca "                quorum01 HCA-2"    558    1[  ] ==( 4X      25.78125 Gbps Active/  LinkUp)==>  0xec0d9a030002b810    496   15[  ] "SwitchIB Mellanox Technologies" ( )
            # 0x248a07030017b12c "                  thing3 HCA-1"    532    1[  ] ==( 4X      25.78125 Gbps Active/  LinkUp)==>  0xec0d9a030002b810    496   19[  ] "SwitchIB Mellanox Technologies" ( )
    
            # break the line into three parts to make the regex simpler
            near, connection, far = line.split('==')
    
    
            #linkRegex =  re.match ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)\[  \] ==\( (\w\w)\s+(\d+.\d+ \w+) (w+\w+).*', near) 
            #linkRegexNear =  re.match ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)', near) 
            #linkRegexConnection =  re.match ( r'\( (\w\w)\s+(\d+.\d+ \w+) (\w+)/\s+(\w+)\)', connection) 
            #linkRegexFar =  re.match ( r'>\s+(\w+)\s+(\d+)\s+(\d+).*\"(.*)\.*"', far) 
    
            linkRegexNear =  linkRegexNearPattern.match(near) 
            linkRegexConnection =  linkRegexConnectionPattern.match(connection)
            linkRegexFar = linkRegexFarPattern.match(far)
    
            near_gid  =  linkRegexNear.group(1) 
            near_card_type = linkRegexNear.group(2) 
            near_lid_number =  linkRegexNear.group(3) 
            near_port_number =  linkRegexNear.group(4) 
    
            link_ib_type =  linkRegexConnection.group(1) 
            link_rate =  linkRegexConnection.group(2) 
            link_active =  linkRegexConnection.group(3) 
            link_up =  linkRegexConnection.group(4) 
    
            far_gid =  linkRegexFar.group(1) 
            far_lid_number =  linkRegexFar.group(2) 
            far_port_number =  linkRegexFar.group(3) 
            far_name = linkRegexFar.group(4) 
    
            LINKS[near_gid] = {
                    'near_port_number': near_port_number, 
                    'near_card_type': near_card_type, 
                    'near_lid_number': near_lid_number, 
                    'near_port_number': near_port_number,
                    'link_ib_type': link_ib_type,
                    'link_rate' : link_rate,
                    'link_active':link_active,
                    'link_up': link_up,
                    'far_gid': far_gid,
                    'far_lid_number': far_lid_number,
                    'far_port_number': far_port_number,
                    'far_name': far_name,
                    }
    
    
            
            #print(link_ib_type, link_rate, link_active, link_up, far_gid, far_lid_number, far_port_number, far_name)

##################################
##################################
# collect all the input data
process_switch_file( switchTxtFile )
process_host_file( hostTxtFile )
process_links_file( linkTxtFile )

# 
# create (munin) -[: pings ]-> (alpha)


# create host nodes 
for uid, value in HOSTS.items(): 
    # print neo4j comands to create nodes
    # CREATE (n:Person { name: 'Andy', title: 'Developer' })
    current_name = value['name']
    current_ports = value['ports']
    print(f'CREATE (uid:{uid} {{ type: \'host\', name: \'{current_name}\', ports: {current_ports} }} ) ' )

# create switches nodes 
for uid, value in SWITCHES.items(): 
    # print neo4j comands to create nodes
    # CREATE (n:Person { name: 'Andy', title: 'Developer' })
    current_name = value['name']
    current_ports = value['ports']
    print(f'CREATE (uid:{uid} {{ type: \'switch\', name: \'{current_name}\', ports: {current_ports} }} ) ' )

# create links 
for uid, value in LINKS.items(): 
    #{'near_port_number': '1', 'near_card_type': 'thing4 HCA-1', 'near_lid_number': '612', 'link_ib_type': '4X', 'link_rate': '25.78125 Gbps', 'link_active': 'Active', 'link_up': 'LinkUp', 'far_gid': '0xec0d9a030002b810', 'far_lid_number': '496', 'far_port_number': '20', 'far_name': 'SwitchIB Mellanox Technologies'}    
    #print( uid, value['near_port_number'] )
    print(f'CREATE (uid:{uid}) -[:' )
