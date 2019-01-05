#! /usr/bin/env python3

import os
import re

hostFile = 'ibhosts.txt'	
#linkFile = 'iblinkinfo.txt'
linkFile = 'test.txt'
switchFile = 'ibswitches.txt'

# links' key is the 'near' gid
# near gid --> connection --> far gid
links = {}
hosts = {}
switches = {}

switchRegexPattern = re.compile ( r'\w+\s+: (\w+) ports (\d+) \"(.*)\" .*') 
hostRegexPattern = re.compile ( r'\w+\s+: (\w+) ports (\d+) \"(.*)\"' ) 
linkRegexNearPattern =  re.compile ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)') 
linkRegexConnectionPattern =  re.compile ( r'\( (\w\w)\s+(\d+.\d+ \w+) (\w+)/\s+(\w+)\)') 
linkRegexFarPattern =  re.compile ( r'>\s+(\w+)\s+(\d+)\s+(\d+).*\"(.*)\.*"') 


with open(switchFile) as switchFileHandle:
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
        switches[gid] = [name, ports,] 
        #print(gid, name, ports)
    
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
        hosts[gid] = [name, ports,] 
        #print(gid, name, ports)

with open(linkFile) as linkFileHandle:
    for line in linkFileHandle:
        # example input:
        # 0x248a07030017b128 "                  thing4 HCA-1"    612    1[  ] ==( 4X      25.78125 Gbps Active/  LinkUp)==>  0xec0d9a030002b810    496   20[  ] "SwitchIB Mellanox Technologies" ( )
        # 0xec0d9a03006ed0ca "                quorum01 HCA-2"    558    1[  ] ==( 4X      25.78125 Gbps Active/  LinkUp)==>  0xec0d9a030002b810    496   15[  ] "SwitchIB Mellanox Technologies" ( )
        # 0x248a07030017b12c "                  thing3 HCA-1"    532    1[  ] ==( 4X      25.78125 Gbps Active/  LinkUp)==>  0xec0d9a030002b810    496   19[  ] "SwitchIB Mellanox Technologies" ( )

        print("----",line)
        # break the line into three parts to make the regex simpler
        near, connection, far = line.split('==')
        print("----",far)


        #linkRegex =  re.match ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)\[  \] ==\( (\w\w)\s+(\d+.\d+ \w+) (w+\w+).*', near) 
        linkRegexNear =  re.match ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)', near) 
        # ( 4X      25.78125 Gbps Active/  LinkUp)
        linkRegexConnection =  re.match ( r'\( (\w\w)\s+(\d+.\d+ \w+) (\w+)/\s+(\w+)\)', connection) 
        # >  0xec0d9a030002b810    496   20[  ] "SwitchIB Mellanox Technologies" ( )
        #linkRegexFar =  re.match ( r'(\w+)\s+\"\s+(.*)\"\s+(\d+)\s+(\d+)', far) 
        linkRegexFar =  re.match ( r'>\s+(\w+)\s+(\d+)\s+(\d+).*\"(.*)\.*"', far) 

        #lineRegex = lineRegexPattern.match ( line ) 
        #gid  =  linkRegexNear.group(1) 
        #card = linkRegexNear.group(2) 
        #lid_number =  linkRegexNear.group(3) 
        #port_number =  linkRegexNear.group(4) 

        #ib_type =  linkRegexConnection.group(1) 
        #link_rate =  linkRegexConnection.group(2) 
        #link_active =  linkRegexConnection.group(3) 
        #link_up =  linkRegexConnection.group(4) 

        #far_gid =  linkRegexFar.group(1) 
        #far_lid_number =  linkRegexFar.group(2) 
        #far_port_number =  linkRegexFar.group(3) 
        #far_name = linkRegexFar.group(4) 


        

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

        links[near_gid] = {
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



