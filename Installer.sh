#!/bin/bash

# Hentikan skrip jika ada ralat
set -e

# Kemas kini sistem
echo "🔧 Mengemas kini sistem..."
sudo apt update

# Pasang keperluan
echo "📦 Memasang Python 3, pip, dan virtualenv..."
sudo apt install -y python3 python3-pip python3-venv

# Tukar ke folder projek
PROJECT_DIR=~/Documents/EXERCISE/Log_Analyzer
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
else
    echo "❌ Folder projek tidak dijumpai: $PROJECT_DIR"
    exit 1
fi

# Cipta virtual environment jika belum wujud
if [ ! -d "venv" ]; then
    echo "🐍 Mencipta virtual environment..."
    python3 -m venv venv
fi

# Aktifkan virtual environment
echo "✅ Mengaktifkan virtual environment..."
source venv/bin/activate

# Pasang kebergantungan Python
echo "📜 Memasang kebergantungan Python..."
pip install --upgrade pip
pip install -r Requirement.txt

# Jalankan sistem
echo "🚀 Menjalankan log analyzer..."
streamlit run System.py
