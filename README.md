# devopsfetch

## Overview
devopsfetch is a DevOps tool for retrieving and monitoring system information, including active ports, user logins, Nginx configurations, Docker images, and container statuses.

## Installation
1. Clone the repository:
    ```bash
    git clone <repo_url>
    cd devopsfetch
    ```

2. Run the installation script:
    ```bash
    sudo ./install.sh
    ```

## Usage
- Display all active ports and services:
    ```bash
    sudo ./devopsfetch.sh -p
    ```

- Display detailed information about a specific port:
    ```bash
    sudo ./devopsfetch.sh -p <port_number>
    ```

- List all Docker images and containers:
    ```bash
    sudo ./devopsfetch.sh -d
    ```

- Display detailed information about a specific container:
    ```bash
    sudo ./devopsfetch.sh -d <container_name>
    ```

- Display all Nginx domains and their ports:
    ```bash
    sudo ./devopsfetch.sh -n
    ```

- Display detailed configuration for a specific domain:
    ```bash
    sudo ./devopsfetch.sh -n <domain>
    ```

- List all users and their last login times:
    ```bash
    sudo ./devopsfetch.sh -u
    ```

- Display detailed information about a specific user:
    ```bash
    sudo ./devopsfetch.sh -u <username>
    ```

- Display activities within a specified time range:
    ```bash
    sudo ./devopsfetch.sh -t '2024-07-22 00:00:00' '2024-07-22 23:59:59'
    ```

## Logging
Logging is not implemented in this version.
