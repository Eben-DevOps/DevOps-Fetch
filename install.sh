#!/bin/bash

# Install dependencies
pip3 install -r requirements.txt

# Copy the systemd service file to the appropriate location
cp devopsfetch.service /etc/systemd/system/

# Reload systemd manager configuration
systemctl daemon-reload

# Enable the service to start on boot
systemctl enable devopsfetch.service

# Start the service
systemctl start devopsfetch.service

echo "Installation complete. The devopsfetch service is now running."
