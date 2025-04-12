#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python not found. Installing the latest version..."
    # Update package list and install Python
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
    echo "Python installed successfully!"
else
    echo "Python is already installed."
fi

# Install dependencies (if needed)
pip3 install -r Requirements.txt

# Run the system.py script
python3 System.py
