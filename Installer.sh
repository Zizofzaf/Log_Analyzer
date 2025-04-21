#!/bin/bash

# Pastikan skrip berhenti jika ada kesalahan
set -e

# Kemas kini sistem
echo "🔧 Mengemas kini sistem..."
sudo apt update

# Pasang keperluan
echo "📦 Memasang Python 3, pip, dan virtualenv..."
sudo apt install -y python3 python3-pip python3-venv

# Tukar ke folder projek (ubah laluan mengikut folder projek anda)
cd ~/Documents/EXERCISE/Log_Analyzer || { echo "❌ Folder projek tidak dijumpai"; exit 1; }

# Cipta virtual environment
echo "🐍 Mencipta virtual environment..."
python3 -m venv venv

# Aktifkan virtual environment
echo "✅ Mengaktifkan virtual environment..."
source venv/bin/activate

# Pasang kebergantungan Python
echo "📜 Memasang kebergantungan Python..."
pip install --upgrade pip
pip install -r Requirement.txt

# Jalankan sistem (atau mana-mana fail yang anda mahu)
echo "🚀 Menjalankan log analyzer..."
streamlit run System.py
