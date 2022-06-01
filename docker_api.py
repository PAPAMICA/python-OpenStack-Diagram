#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import docker
import json

arg_dict = 1
arg_json = 0

client = docker.from_env()



def get_containers_list():
    c_all = client.containers.list(all)
    allcontainers = list()
    for c in c_all:
        allcontainers.append(c.name)
    if arg_json == 1:
        result = json.dumps(allcontainers, indent=4)
    else:
        result = allcontainers
    return result


def get_container_informations(container):
    try:
        c = client.containers.get(container)
    except:
        return (f"ERROR: {container} doesn't exist !")
    # Status
    status = c.attrs['State']['Status']

    # Health
    if str(c.attrs['State']).find("Health") == -1:
        health = None
    else:
        health = c.attrs['State']['Health']['Status']
        
    # Bind
    if str(c.attrs['HostConfig']).find("Binds") == -1:
        binds = None
    else:
        binds = c.attrs['HostConfig']['Binds']
        
    # Network
    if str(c.attrs['HostConfig']).find("NetworkMode") == -1:
        network = None
    else:
        network = c.attrs['HostConfig']['NetworkMode']
        
    # Ports
    if str(c.attrs['HostConfig']).find("PortBindings") == -1:
        ports = None
    else:
        ports_temp = c.attrs['HostConfig']['PortBindings']
        ports = list()
        for i in ports_temp:
            ports.append(i)
            
    # Image
    image = c.attrs['Config']['Image']
            
    # IPadress
    ipadress = c.attrs['NetworkSettings']['Networks'][network]['IPAddress']

    data = {'container': container}
    data['Status'] = status
    data['Health'] = health
    data['Binds'] = binds
    data['Network'] = network
    data['IP'] = ipadress
    data['Ports'] = ports
    data['Image'] = image
    

    if arg_dict == 1:
        result = {}
    else:
        result = ""
    if arg_dict == 1:
        result[container] = data
    elif arg_json == 1:
        data = json.dumps(data, indent=4)
        result = result + data
    else:
        result = str(result) + f"{c.name} -\n Status: {status} ({health})\n Binds: {binds}\n Network: {network}\n IP:{ipadress}\n Ports: {ports} \n Image: {image}\n"
    return result

def get_networks_list():
    n_all = client.networks.list()
    allnetworks = list()
    for n in n_all:
        allnetworks.append(n.name)
    if arg_json == 1:
        result = json.dumps(allnetworks, indent=4)
    else:
        result = allnetworks
    return result


def get_network_informations(network):
    try:
        n = client.networks.get(network)
    except:
        return (f"ERROR: {network} doesn't exist !")

    # Stack
    Labels = n.attrs['Labels']
    if str(Labels).find("project") == -1:
        stack = None
    else:
        stack = n.attrs['Labels']['com.docker.compose.project']

    # Driver    
    driver = n.attrs['Driver']

    # Subnet
    if str(n.attrs['IPAM']['Config']).find("Subnet") == -1:
        subnet = None
    else:
        subnet = n.attrs['IPAM']['Config'][0]['Subnet']

    # Containers
    containers = list()
    container = dict()
    for i in n.attrs['Containers']: 
        container['Container'] = n.attrs['Containers'][i]['Name']
        container['IPv4'] = n.attrs['Containers'][i]['IPv4Address']
        containers.append(container)
        
    data = {'network': network}
    data['Subnet'] = subnet
    data['Stack'] = stack
    data['Containers'] = containers
    

    if arg_dict == 1:
        result = {}
    else:
        result = ""
    if arg_dict == 1:
        result[network] = data
    elif arg_json == 1:
        data = json.dumps(data, indent=4)
        result = result + data
    else:
        result = str(result) + f"- {n.name} -\n Subnet: {subnet}\n Driver: {driver}\n Stack: {stack}\n Containers: {containers}"
    return result
    