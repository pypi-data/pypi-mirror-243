#!/bin/bash

# Define the service name
SERVICE_NAME="your-service-name"

# Get the systemd system unit directory
SYSTEMD_DIR=$(pkg-config systemd --variable=systemdsystemunitdir)

# Generate the service file path
SERVICE_FILE="${SYSTEMD_DIR}/${SERVICE_NAME}.service"

# Define the service content
SERVICE_CONTENT="[Unit]
Description=Your Service Description
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/your-script-or-command

[Install]
WantedBy=default.target
"

# Write the content to the service file
echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE" > /dev/null
