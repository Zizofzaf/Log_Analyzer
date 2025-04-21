#!/bin/bash

# Exit the script immediately if any command fails
set -e

# Update the system
echo "🔧 Updating the system..."
sudo apt update

# Install required packages
echo "📦 Installing Python 3, pip, and virtualenv..."
sudo apt install -y python3 python3-pip python3-venv

# Change to the project directory (modify this path according to your project folder)
cd ~/Documents/EXERCISE/Log_Analyzer || { echo "❌ Project folder not found"; exit 1; }

# Create a virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📜 Installing Python dependencies..."
pip install --upgrade pip
pip install -r Requirement.txt

# Run the system (or any file you want to execute)
echo "🚀 Running log analyzer..."
streamlit run System.py
