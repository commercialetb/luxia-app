# 🚀 INIZIA QUI - LUXiA v1.0

Benvenuto in **LUXiA**, l'applicazione per la progettazione illuminotecnica avanzata!

## ⚡ Quick Start (2 minuti)

### 1️⃣ Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 2️⃣ Avvia l'App
```bash
streamlit run app.py
```

### 3️⃣ Apri nel Browser
Vai a: **http://localhost:8501**

## 📖 Documentazione

| File | Argomento |
|------|-----------|
| **GUIDA_RAPIDA.md** | Come usare l'app (tutorial completo) |
| **README.md** | Documentazione tecnica |
| **DEVELOPER.md** | Per sviluppatori che vogliono estendere il progetto |
| **CHANGELOG.md** | Cronologia versioni e roadmap |

## 🎯 Primo Progetto - Guida Step-by-Step

### Scenario: Illuminare un Salotto 5m × 4m

#### Step 1: Prepara i File
1. **Planimetria**: Scatta una foto del salotto (JPG) oppure esporta da CAD
2. **Fotometria**: Scarica il file `.ldt` della tua lampada dal sito del produttore
   - Esempio: `Artemide_Tolomeo.ldt`

#### Step 2: Carica nella App
1. Apri app (http://localhost:8501)
2. **STEP 1**: Click "Carica planimetria" → seleziona foto JPG
3. **STEP 2**: Click "Carica fotometria" → seleziona file `.ldt`

#### Step 3: Disegna Area
1. **STEP 3**: 
   - **Nome Area**: `Salotto Principale`
   - **Altezza Montaggio**: `2.7m` (tipico salotto)
   - **Altezza Piano Calcolo**: `0.85m` (altezza sofà)
   - **Seleziona Fotometria**: la lampada caricata
   - Click **"Aggiungi Area"**

#### Step 4: Visualizza Risultati
1. **STEP 4**: Vedi automaticamente:
   - Larghezza fascio: es. `2.8m`
   - Lampade necessarie: es. `6` (disposizione 2×3)
   - Spaziamento: `2.5m × 1.9m`

#### Step 5: Scarica Risultati
1. **Scarica PDF Report**: Riepilogo completo con tabelle
2. **Scarica DWG Layout**: Apri in AutoCAD per vedere la planimetria con lampade

## 💡 Consigli Pratici

### Come Trovare il File LDT
- **Sito Produttore**: La maggior parte fornisce file LDT
  - Artemide: www.artemide.com
  - Flos: www.flos.com
  - Luceplan: www.luceplan.com
  - iGuzzini: www.iguzzini.com
  
- **GenIO IES**: Converte IES a LDT
- **Contatta il Fornitore**: Se non lo trovi online

### Parametri Tipici

**Salotto**
- Altezza montaggio: 2.7m
- Piano calcolo: 0.85m
- Angolo fascio: 20-30°

**Cucina**
- Altezza montaggio: 2.5m
- Piano calcolo: 0.9m (piano lavoro)
- Angolo fascio: 15-25°

**Ufficio**
- Altezza montaggio: 3.0m
- Piano calcolo: 0.75m (scrivania)
- Angolo fascio: 15-20°

**Corridoio**
- Altezza montaggio: 2.6m
- Piano calcolo: 0.0m (suolo)
- Angolo fascio: 30-40°

### Verificare i Risultati
- ✅ Numero lampade ragionevole? (1-2 per 5-10 m²)
- ✅ Spaziamento coerente? (generalmente 2-4 metri)
- ✅ Uniformità >80%? (buon compromesso)

Se i numeri sembrano strani:
1. Ricontrolla altezze (confusione m vs cm?)
2. Verifica angolo fascio dal datasheet
3. Prova con area di superficie minore

## 🔧 Troubleshooting

### Problema: "Cartella output non trovata"
**Soluzione**: La cartella `outputs/` viene creata automaticamente

### Problema: "LDT non si carica"
**Soluzione**:
1. Verifica che sia un vero file `.ldt`
2. Prova ad aprirlo con editor testo (deve contenere numeri)
3. Se corrotto, riscarica da sito produttore

### Problema: "PDF scarica vuoto"
**Soluzione**:
1. Assicurati di aver aggiunto almeno un'area (STEP 3)
2. Seleziona una fotometria caricata
3. Ripeti il download

### Problema: "DWG non si apre in AutoCAD"
**Soluzione**:
1. Prova ad aprire con File → Open
2. Se non legge, converti il DWG in questo sito:
   - https://cloudconvert.com (DWG → DXF)
3. Apri il DXF in AutoCAD

## 📞 Supporto

- **Domande Frecenti**: Leggi GUIDA_RAPIDA.md sezione "Troubleshooting"
- **Bug Report**: Apri un issue su GitHub
- **Suggerimenti**: Discussioni GitHub

## 📊 Struttura File Progetto

```
luxia-app/
├── app.py                    # App principale
├── config.py                 # Configurazione
├── requirements.txt          # Dipendenze
├── test_luxia.py            # Test suite
├── setup.sh                 # Script setup
├── README.md                # Documentazione
├── GUIDA_RAPIDA.md          # Quick start guide
├── DEVELOPER.md             # Per sviluppatori
├── CHANGELOG.md             # Versioni
├── LICENSE                  # MIT License
├── outputs/                 # Cartella PDF/DWG output
└── utils/
    ├── photometry.py        # Parser LDT
    ├── blueprint_processor.py # Gestione immagini
    ├── lamp_calculator.py    # Calcoli lampade
    └── report_generator.py   # Generazione PDF
```

## ⚖️ Avvertenza Legale

**IMPORTANTE**: I calcoli di LUXiA sono preliminari e semplificati.

Per progetti professionali:
1. ✅ Verifica SEMPRE con software certificato
2. ✅ Effettua misurazioni in situ
3. ✅ Consulta un professionista illuminotecnico
4. ✅ Conformati alle normative locali

Leggi il file LICENSE per disclaimer completo.

## 🎓 Prossimi Passi

1. ✅ Prova il primo progetto (vedi sopra)
2. 📖 Leggi GUIDA_RAPIDA.md per dettagli
3. 🔍 Esplora le impostazioni in `config.py`
4. 🧪 Esegui il test suite: `python test_luxia.py`
5. 💻 Leggi DEVELOPER.md se vuoi modificare il codice

## 🆘 Non Funziona?

1. Verifica che Python 3.8+ sia installato: `python --version`
2. Verifica che le dipendenze siano installate: `pip list | grep streamlit`
3. Esegui il test suite: `python test_luxia.py`
4. Leggi il GUIDA_RAPIDA.md sezione Troubleshooting
5. Apri un issue su GitHub

## 🎉 Buon Lavoro!

Grazie di aver scelto LUXiA. Che tu stia progettando un'illuminazione residenziale, commerciale o industriale, questa app ti aiuterà a trovare rapidamente il numero di lampade necessarie e il loro corretto posizionamento.

Ricorda: **I risultati sono preliminari. Verifica sempre con professionisti certificati e normative locali!**

---

**Versione**: 1.0  
**Data**: Gennaio 2026  
**Licenza**: MIT  
**Stato**: ✅ Stabile e Pronto all'Uso

Domande? Apri un issue su GitHub! 🚀
