#!/bin/bash

# Warna untuk output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting installation...${NC}"

# 1. Update dan install Python serta pip (jika belum ada)
echo -e "${GREEN}Checking for Python...${NC}"
if ! command -v python3 &> /dev/null
then
    echo -e "${GREEN}Python3 not found. Installing...${NC}"
    sudo apt update
    sudo apt install python3 -y
fi

echo -e "${GREEN}Checking for pip...${NC}"
if ! command -v pip3 &> /dev/null
then
    echo -e "${GREEN}pip not found. Installing...${NC}"
    sudo apt install python3-pip -y
fi

# 2. Create virtual environment (optional tapi recommended)
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install -r Requirement.txt

# 4. Run system
echo -e "${GREEN}Running system...${NC}"
python3 System.py
