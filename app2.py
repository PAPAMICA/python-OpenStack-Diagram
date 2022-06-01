#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import docker_api as docker
import argparse
from diagrams import Diagram, Cluster
from diagrams.custom import Custom

parser = argparse.ArgumentParser(description='Create a graph of your Docker project.')
parser.add_argument("--container", required=False, help='Create a graph of one container')
parser.add_argument("--network", required=False, help='Create a graph of one network')
args = parser.parse_args()

graph_attr = {
    "layout": "dot",
}
tag_attr = {
    "center": "true",
    "layout": "fdp",
    "imagepos": "mc"
}
edge_attr = {
    "minlen":"2",
}



def create_diagram():
    with Diagram("\nDocker infrastructure", show=True, direction="TB", graph_attr=graph_attr, node_attr=tag_attr,edge_attr=edge_attr) as diag:
        img_network = Custom(f"{args.network}\nSubnet: {_network[args.network]['Subnet']}", "./img/internet.png")
        containers = []
        for container in _network[args.network]['Containers']:
            img_container = Custom(
                f"{container['Container']}\n IP : {container['IPv4']}", "./img/container.png")
            
            containers.append(img_container)

            
        img_network >> img_container 

       
    diag


if args.container:
    print(docker.get_container_informations(args.container))
elif args.network:
    _network = docker.get_network_informations(args.network)
    create_diagram()