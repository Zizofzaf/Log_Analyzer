#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Log Analyzer installation...${NC}"

# 1. Check for Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${GREEN}Python3 not found. Installing...${NC}"
    sudo apt update
    sudo apt install python3 -y
fi

# 2. Check for pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${GREEN}pip3 not found. Installing...${NC}"
    sudo apt install python3-pip -y
fi

# 3. Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv

# 4. Activate venv
source venv/bin/activate

# 5. Install requirements
echo -e "${GREEN}Installing required Python packages...${NC}"
pip install --upgrade pip
pip install -r Requirement.txt

# 6. Run system.py
echo -e "${GREEN}Running Log Analyzer...${NC}"
python system.py
