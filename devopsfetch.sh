#!/bin/bash

# Ensure the script is run with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

function list_ports() {
    ss -tuln | awk 'NR>1 {print $1, $4, $6}'
}

function port_details() {
    lsof -i :$1
}

function list_docker() {
    docker ps -a
    docker images
}

function container_details() {
    docker inspect $1
}

function list_nginx() {
    grep -r "server_name" /etc/nginx/sites-enabled/
}

function nginx_details() {
    nginx -T | grep -A 20 "server_name $1;"
}

function list_users() {
    lastlog
}

function user_details() {
    lastlog -u $1
}

function activities_within_time_range() {
    journalctl --since "$1" --until "$2"
}

function show_help() {
    echo "Usage: $0 [options]
Options:
  -p, --port [PORT]      Display all active ports and services or details of a specific port
  -d, --docker [CONTAINER]   List all Docker images and containers or details of a specific container
  -n, --nginx [DOMAIN]    Display all Nginx domains and ports or details of a specific domain
  -u, --users [USERNAME]  List all users and their last login times or details of a specific user
  -t, --time START END    Display activities within a specified time range
  -l, --log               Enable continuous monitoring and logging
  -h, --help              Show this help message"
}

while [[ "$1" != "" ]]; do
    case $1 in
        -p | --port )           shift
                                if [[ -z "$1" ]]; then
                                    list_ports
                                else
                                    port_details $1
                                fi
                                exit
                                ;;
        -d | --docker )         shift
                                if [[ -z "$1" ]]; then
                                    list_docker
                                else
                                    container_details $1
                                fi
                                exit
                                ;;
        -n | --nginx )          shift
                                if [[ -z "$1" ]]; then
                                    list_nginx
                                else
                                    nginx_details $1
                                fi
                                exit
                                ;;
        -u | --users )          shift
                                if [[ -z "$1" ]]; then
                                    list_users
                                else
                                    user_details $1
                                fi
                                exit
                                ;;
        -t | --time )           shift
                                if [[ -z "$1" || -z "$2" ]]; then
                                    echo "Please provide start and end time"
                                else
                                    activities_within_time_range "$1" "$2"
                                fi
                                exit
                                ;;
        -l | --log )            echo "Continuous monitoring not implemented in this version."
                                exit
                                ;;
        -h | --help )           show_help
                                exit
                                ;;
        * )                     show_help
                                exit 1
    esac
    shift
done
show_help
