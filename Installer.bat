@echo off
echo ====================================
echo       🚀 Setup Sistem Bermula
echo ====================================

REM Semak Python
where python >nul 2>nul
IF ERRORLEVEL 1 (
    echo ❌ Python tidak dijumpai. Sila pasang dahulu.
    pause
    exit /b
)

REM Semak untuk install python3-venv
echo 🔍 Memeriksa keperluan untuk `venv`...
python -m venv --help >nul 2>nul
IF ERRORLEVEL 1 (
    echo ❌ Modul venv tidak dijumpai. Memasang python3-venv...
    python -m pip install --upgrade pip
    python -m pip install virtualenv
)

REM Buat virtual environment jika belum ada
IF NOT EXIST venv (
    echo 🔧 Membuat virtual environment...
    python -m venv venv
) ELSE (
    echo ✅ Virtual environment sedia ada dijumpai.
)

REM Aktifkan venv
echo ⚙️ Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip dan install keperluan
echo 📦 Memasang dependencies...
python -m pip install --upgrade pip

IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    echo ❗ requirements.txt tidak dijumpai!
)

REM Jalankan Streamlit App
IF EXIST app.py (
    echo 🚀 Menjalankan aplikasi Streamlit...
    start "" http://localhost:8501
    streamlit run app.py
) ELSE (
    echo ❗ app.py tidak dijumpai!
)

echo ====================================
echo       ✅ Setup Selesai!
echo       Untuk aktifkan venv semula:
echo       venv\Scripts\activate.bat
echo ====================================
pause
