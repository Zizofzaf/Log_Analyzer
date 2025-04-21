#!/bin/bash

# Installer.sh – Setup script untuk sistem Python

echo "===================================="
echo "     Sistem Setup Bermula..."
echo "===================================="

# Semak jika Python dipasang
if ! command -v python3 &> /dev/null; then
    echo "Python3 tidak dijumpai. Sila pasang Python3 dahulu."
    exit 1
fi

# Semak jika pip dipasang
if ! command -v pip3 &> /dev/null; then
    echo "pip3 tidak dijumpai. Sila pasang pip dahulu."
    exit 1
fi

# Buat virtual environment
echo "Membuat virtual environment..."
python3 -m venv venv

# Aktifkan virtual environment
echo "Aktifkan virtual environment..."
source venv/bin/activate

# Pasang keperluan dari requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Memasang dependencies dari requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt tidak dijumpai!"
    exit 1
fi

# Jalankan sistem (contohnya app.py)
echo "Menjalankan sistem..."
python app.py  # atau streamlit run app.py jika guna Streamlit

echo "===================================="
echo "     Setup Selesai! Sistem Ready."
echo "===================================="
