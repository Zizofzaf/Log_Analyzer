#!/bin/bash

# Update system
echo "Updating system..."
sudo apt update

# Install dependencies (adjust according to your needs)
echo "Installing Python 3, pip, and other dependencies..."
sudo apt install -y python3 python3-pip

# Clone the repository (optional if you want to automatically download the project)
echo "Cloning project from GitHub..."
git clone https://github.com/Zizofzaf/Log_Analyzer

# Navigate to project folder
cd repo_name

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r Requirements.txt

# Run the system (or any specific file you want)
echo "Running the log analyzer..."
python3 System.py
