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
    ./install.sh
    ```

## Usage
- Display all active ports and services:
    ```bash
    ./devopsfetch.py -p
    ```

- Display detailed information about a specific port:
    ```bash
    ./devopsfetch.py -p <port_number>
    ```

- List all Docker images and containers:
    ```bash
    ./devopsfetch.py -d
    ```

- Display detailed information about a specific container:
    ```bash
    ./devopsfetch.py -d <container_name>
    ```

- Display all Nginx domains and their ports:
    ```bash
    ./devopsfetch.py -n
    ```

- Display detailed configuration for a specific domain:
    ```bash
    ./devopsfetch.py -n <domain>
    ```

- List all users and their last login times:
    ```bash
    ./devopsfetch.py -u
    ```

- Display detailed information about a specific user:
    ```bash
    ./devopsfetch.py -u <username>
    ```

- Display activities within a specified time range:
    ```bash
    ./devopsfetch.py -t '2024-07-22 00:00:00' '2024-07-22 23:59:59'
    ```

## Logging
Logs are written to `/var/log/devopsfetch.log`. Log rotation and management are handled by the logging module.

## Continuous Monitoring
The `devopsfetch` tool can run as a continuous monitoring service, logging activities to a file:
```bash
./devopsfetch.py -l



### Next Steps
**a.** Add unit tests to ensure the functionality of each component.
**b.** Implement a more sophisticated time range filtering for activities by parsing system logs.

