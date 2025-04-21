#!/bin/bash

echo "===================================="
echo "     🚀 Setup Sistem Bermula"
echo "===================================="

# Semak jika Python dipasang
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak dijumpai. Sila pasang dahulu."
    exit 1
fi

# Semak jika pip dipasang
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 tidak dijumpai. Sila pasang dahulu."
    exit 1
fi

# Buat virtual environment jika belum ada
if [ ! -d "venv" ]; then
    echo "🔧 Membuat virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment sedia ada dijumpai."
fi

# Aktifkan venv
echo "⚙️  Mengaktifkan virtual environment..."
source venv/bin/activate

# Upgrade pip dan install requirements
echo "📦 Memasang dependencies..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❗ requirements.txt tidak dijumpai. Teruskan tanpa install dependencies fail."
fi

# Jalankan Streamlit App
if [ -f "app.py" ]; then
    echo "🚀 Menjalankan aplikasi Streamlit..."

    # Jalankan dalam background & buka browser
    streamlit run app.py &

    # Tunggu server ready sebelum buka browser (anggaran 3 saat)
    sleep 3

    # Buka dalam browser default
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8501
    elif command -v open &> /dev/null; then
        open http://localhost:8501  # untuk macOS
    else
        echo "📎 Sila buka pelayar dan pergi ke: http://localhost:8501"
    fi
else
    echo "❗ app.py tidak dijumpai!"
fi

echo "===================================="
echo "     ✅ Setup Siap! Enjoy 🚀"
echo "     Untuk aktifkan semula venv:"
echo "     source venv/bin/activate"
echo "===================================="
