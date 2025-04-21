#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Log Analyzer installation...${NC}"

# 1. Auto-pull latest changes
echo -e "${GREEN}Checking for updates...${NC}"
git pull origin main

# 2. Check for Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${GREEN}Python3 not found. Installing...${NC}"
    sudo apt update
    sudo apt install python3 -y
fi

# 3. Check for pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${GREEN}pip3 not found. Installing...${NC}"
    sudo apt install python3-pip -y
fi

# 4. Check if virtual environment already exists
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
else
    echo -e "${GREEN}Virtual environment found. Skipping creation...${NC}"
fi

# 5. Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# 6. Install requirements
echo -e "${GREEN}Installing required Python packages...${NC}"
pip install --upgrade pip
pip install -r Requirement.txt

# 7. Run system.py
echo -e "${GREEN}Running Log Analyzer...${NC}"
python System.py
