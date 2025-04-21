#!/bin/bash

echo "===================================="
echo "     Sistem Setup Bermula..."
echo "===================================="

# Semak jika Python dipasang
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak dijumpai. Sila pasang Python3 dahulu."
    exit 1
fi

# Semak jika pip dipasang
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 tidak dijumpai. Sila pasang pip dahulu."
    exit 1
fi

# Buat virtual environment jika belum ada
if [ ! -d "venv" ]; then
    echo "🔧 Membuat virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment sudah wujud."
fi

# Aktifkan virtual environment
echo "⚙️  Aktifkan virtual environment..."
source venv/bin/activate

# Pasang keperluan dari requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Memasang dependencies dari requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "❌ requirements.txt tidak dijumpai!"
    exit 1
fi

if [ -f "app.py" ]; then
    echo "🚀 Menjalankan sistem Streamlit..."
    streamlit run app.py
else
    echo "ℹ️  app.py tidak dijumpai. Setup selesai tanpa run aplikasi."
fi

echo "===================================="
echo "     ✅ Setup Selesai!"
echo "     Aktifkan semula venv bila perlu:"
echo "     source venv/bin/activate"
echo "===================================="
