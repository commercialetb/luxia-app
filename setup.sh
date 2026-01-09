#!/bin/bash
# Deploy script per LUXiA

echo "╔════════════════════════════════════════════════════════╗"
echo "║         LUXiA - Script di Installazione e Setup       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Verifica Python
echo "1️⃣  Verifica Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installa Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION trovato"
echo ""

# Crea virtual environment
echo "2️⃣  Creazione Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment creato"
else
    echo "✓ Virtual environment già esistente"
fi
echo ""

# Attiva venv
echo "3️⃣  Attivazione Virtual Environment..."
source venv/bin/activate
echo "✓ Virtual environment attivato"
echo ""

# Aggiorna pip
echo "4️⃣  Aggiornamento pip..."
python -m pip install --upgrade pip -q
echo "✓ pip aggiornato"
echo ""

# Installa dipendenze
echo "5️⃣  Installazione Dipendenze..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    echo "✓ Dipendenze installate da requirements.txt"
else
    echo "❌ File requirements.txt non trovato"
    exit 1
fi
echo ""

# Esegui test
echo "6️⃣  Esecuzione Test Suite..."
python test_luxia.py
echo ""

# Informazioni finali
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║               Setup Completato! ✓                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Per avviare l'app, esegui:"
echo ""
echo "    streamlit run app.py"
echo ""
echo "Quindi apri il browser a: http://localhost:8501"
echo ""
echo "Per ulteriore aiuto, leggi GUIDA_RAPIDA.md"
echo ""
