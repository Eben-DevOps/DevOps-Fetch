#!/usr/bin/env python3

import argparse
import subprocess
import pwd
from datetime import datetime
import psutil
import docker
import os
import logging
from logging.handlers import RotatingFileHandler
from tabulate import tabulate

# Configure logging
log_file = '/var/log/devopsfetch.log'
handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()

def list_ports():
    connections = psutil.net_connections()
    data = []
    for conn in connections:
        if conn.laddr:
            data.append([conn.laddr.port, conn.status, conn.pid])
    print(tabulate(data, headers=['Port', 'Status', 'PID'], tablefmt='pretty'))

def port_details(port_number):
    connections = psutil.net_connections()
    data = []
    for conn in connections:
        if conn.laddr and conn.laddr.port == port_number:
            data.append([conn.laddr.port, conn.status, conn.pid])
    print(tabulate(data, headers=['Port', 'Status', 'PID'], tablefmt='pretty'))

def list_docker():
    client = docker.from_env()
    containers = client.containers.list(all=True)
    images = client.images.list()
    container_data = [[container.name, container.status, container.image.tags] for container in containers]
    image_data = [[image.id, image.tags] for image in images]
    print("Containers:")
    print(tabulate(container_data, headers=['Name', 'Status', 'Image Tags'], tablefmt='pretty'))
    print("\nImages:")
    print(tabulate(image_data, headers=['ID', 'Tags'], tablefmt='pretty'))

def container_details(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        print(f"Name: {container.name}")
        print(f"Status: {container.status}")
        print(f"Image: {container.image.tags}")
        print(f"Command: {container.attrs['Config']['Cmd']}")
        print(f"Ports: {container.attrs['NetworkSettings']['Ports']}")
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")

def list_nginx():
    config_path = '/etc/nginx/sites-enabled/'
    data = []
    for conf in os.listdir(config_path):
        with open(os.path.join(config_path, conf), 'r') as file:
            for line in file:
                if 'server_name' in line:
                    domain = line.split()[1].strip(';')
                if 'listen' in line:
                    port = line.split()[1].strip(';')
                    data.append([domain, port])
    print(tabulate(data, headers=['Domain', 'Port'], tablefmt='pretty'))

def nginx_details(domain):
    config_path = '/etc/nginx/sites-enabled/'
    for conf in os.listdir(config_path):
        with open(os.path.join(config_path, conf), 'r') as file:
            lines = file.readlines()
            if any(domain in line for line in lines):
                print(f"Configuration for {domain}:")
                for line in lines:
                    print(line.strip())

def list_users():
    users = pwd.getpwall()
    data = []
    for user in users:
        try:
            last_login = subprocess.check_output(f'lastlog -u {user.pw_name}', shell=True).decode().strip()
            data.append([user.pw_name, last_login])
        except subprocess.CalledProcessError:
            data.append([user.pw_name, "No login found"])
    print(tabulate(data, headers=['Username', 'Last Login'], tablefmt='pretty'))

def user_details(username):
    try:
        last_login = subprocess.check_output(f'lastlog -u {username}', shell=True).decode().strip()
        print(f"Details for {username}:")
        print(last_login)
    except subprocess.CalledProcessError:
        print(f"No details found for {username}")

def activities_within_time_range(start_time, end_time):
    start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    with open(log_file, 'r') as file:
        for line in file:
            timestamp = line.split(' ')[0] + ' ' + line.split(' ')[1]
            log_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
            if start_dt <= log_dt <= end_dt:
                print(line.strip())

def continuous_monitoring():
    logger.info("Starting continuous monitoring...")
    try:
        while True:
            list_ports()
            list_docker()
            list_nginx()
            list_users()
            logger.info("Monitoring cycle completed.")
    except KeyboardInterrupt:
        logger.info("Continuous monitoring stopped.")

def parse_args():
    parser = argparse.ArgumentParser(description='devopsfetch: System Information Retrieval Tool')
    parser.add_argument('-p', '--port', nargs='?', const=True, type=int, help='Display all active ports and services or details of a specific port.')
    parser.add_argument('-d', '--docker', nargs='?', const=True, type=str, help='List all Docker images and containers or details of a specific container.')
    parser.add_argument('-n', '--nginx', nargs='?', const=True, type=str, help='Display all Nginx domains and ports or details of a specific domain.')
    parser.add_argument('-u', '--users', nargs='?', const=True, type=str, help='List all users and their last login times or details of a specific user.')
    parser.add_argument('-t', '--time', nargs=2, metavar=('START', 'END'), help='Display activities within a specified time range.')
    parser.add_argument('-l', '--log', action='store_true', help='Enable continuous monitoring and logging.')
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit.')
    return parser.parse_args()

def main():
    args = parse_args()

    if args.help:
        print("Usage instructions for devopsfetch:")
        print(parser.format_help())
    elif args.port:
        if args.port is True:
            list_ports()
        else:
            port_details(args.port)
    elif args.docker:
        if args.docker is True:
            list_docker()
        else:
            container_details(args.docker)
    elif args.nginx:
        if args.nginx is True:
            list_nginx()
        else:
            nginx_details(args.nginx)
    elif args.users:
        if args.users is True:
            list_users()
        else:
            user_details(args.users)
    elif args.time:
        start_time = args.time[0]
        end_time = args.time[1]
        activities_within_time_range(start_time, end_time)
    elif args.log:
        continuous_monitoring()
    else:
        print("Use -h or --help for usage instructions.")

if __name__ == "__main__":
    main()
