#!/bin/bash

set -e  # Henti jika ada ralat

# === CONFIGURATION ===
GIT_REPO="https://github.com/username/repo-name.git"  # <-- Ganti dengan repo sebenar anda
REPO_NAME=$(basename "$GIT_REPO" .git)
INSTALL_DIR=~/Documents/EXERCISE/$REPO_NAME

# === PERSIAPAN ===
echo "📁 Membuat folder jika belum wujud..."
mkdir -p ~/Documents/EXERCISE

# === CLONE PROJEK ===
if [ ! -d "$INSTALL_DIR" ]; then
    echo "📥 Clone projek dari GitHub..."
    git clone "$GIT_REPO" "$INSTALL_DIR"
else
    echo "✅ Projek sudah ada. Menggunakan salinan sedia ada."
fi

cd "$INSTALL_DIR" || { echo "❌ Gagal masuk ke folder projek."; exit 1; }

# === SISTEM UPDATE & INSTALL DEPENDENCIES ===
echo "🔧 Mengemas kini sistem dan pasang keperluan..."
sudo apt update
sudo add-apt-repository universe -y
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# === VIRTUAL ENV SETUP ===
if [ ! -d "venv" ]; then
    echo "🐍 Mewujudkan virtual environment..."
    python3 -m venv venv
fi

echo "✅ Mengaktifkan virtual environment..."
source venv/bin/activate

# === INSTALL PYTHON REQUIREMENTS ===
echo "📜 Memasang dependencies Python..."
pip install --upgrade pip

if [ -f "Requirement.txt" ]; then
    pip install -r Requirement.txt
else
    echo "❗ Requirement.txt tidak dijumpai."
    exit 1
fi

# === JALANKAN SISTEM ===
if [ -f "System.py" ]; then
    echo "🚀 Menjalankan sistem Log Analyzer..."
    streamlit run System.py
else
    echo "❗ Fail System.py tidak dijumpai."
    exit 1
fi
