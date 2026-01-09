# 💡 LUXiA – Progettazione Illuminotecnica Avanzata

Una moderna applicazione web per il design illuminotecnico che consente di:
- **Caricare planimetrie** (JPG, PNG, PDF, DWG)
- **Selezionare aree** sulla planimetria e assegnare fotometrie diverse
- **Calcolare automaticamente** il numero di lampade necessarie e lo spaziamento
- **Generare report PDF** con riepilogo aree, prodotti e quantità
- **Esportare DXF/DWG** con il posizionamento delle lampade

## 🚀 Caratteristiche

### Step 1: Carica Planimetria
Carica la planimetria del tuo progetto in uno dei formati supportati:
- **JPG/PNG**: Immagini standard (consigliato)
- **PDF**: Prima pagina convertita automaticamente
- **DWG**: Supporto base (esporta come JPG per miglior risultato)

### Step 2: Seleziona Fotometrie
Carica uno o più file di fotometria in formato **LDT** (Eulumdat):
- Il sistema legge automaticamente i dati del fascio luminoso
- Puoi utilizzare fotometrie diverse per aree diverse

### Step 3: Disegna Aree
Sulla planimetria caricata:
- Definisci le aree di interesse (rettangoli o poligoni)
- Assegna una fotometria a ciascuna area
- Imposta l'altezza di montaggio e il piano di calcolo

### Step 4: Calcoli e Export
Il sistema calcola automaticamente:
- **Larghezza fascio**: Basato sull'angolo e l'altezza di montaggio
- **Numero lampade**: Calcolato in base alla superficie e al fascio
- **Spaziamento (passo)**: Ottimizzato per uniformità
- **Uniformità stimata**: Percentuale di copertura

#### Output disponibili:

📄 **PDF Report**
- Riepilogo di tutte le aree analizzate
- Quantità e tipo di lampade per area
- Dati tecnici (altezze, angoli, spaziamenti)
- Fotometrie utilizzate

🎨 **DWG Layout**
- File AutoCAD con aree disegnate
- Posizionamento automatico delle lampade (simboli circolari)
- Layer organizzati (Areas, Lamps, Grid)

## 📋 Requisiti

- Python 3.8+
- Dipendenze elencate in `requirements.txt`

## 🛠️ Installazione

```bash
# Clona il repository
git clone <your-repo>
cd luxia-app

# Installa dipendenze
pip install -r requirements.txt

# Esegui l'app
streamlit run app.py
```

## 📦 Dipendenze Principali

| Pacchetto | Versione | Scopo |
|-----------|----------|-------|
| `streamlit` | - | Framework web |
| `fpdf2` | - | Generazione PDF |
| `pillow` | - | Elaborazione immagini |
| `opencv-python` | - | Visione artificiale |
| `ezdxf` | - | Creazione file DWG |
| `pdf2image` | - | Conversione PDF → Immagine |
| `numpy`, `pandas` | - | Calcoli numerici |

## 🎯 Flusso di Lavoro Tipico

1. **Carica planimetria JPG/PNG** della tua stanza/area
2. **Carica 1-2 fotometrie LDT** dei tuoi apparecchi illuminanti
3. **Disegna rettangoli** (o poligoni) sulle aree che vuoi illuminare
4. **Assegna fotometria** a ciascuna area
5. **Inserisci altezza montaggio** (es. 3.0 m) e **piano di calcolo** (es. 0.85 m = piano di lavoro)
6. **Clicca "Aggiungi Area"** per ogni zona
7. **Scarica PDF** con il riepilogo completo
8. **Scarica DWG** per visualizzare il layout in AutoCAD

## 📐 Formule di Calcolo

### Larghezza del Fascio
```
beam_width = 2 × (h - hc) × tan(δ)
```
Dove:
- `h` = altezza di montaggio (m)
- `hc` = altezza piano di calcolo (m)
- `δ` = angolo di semiapertura del fascio (°)

### Numero di Lampade
```
spacing = beam_width × 0.7  # Sovrapposizione 30%
n_x = ceil(area_width / spacing)
n_y = ceil(area_height / spacing)
n_total = n_x × n_y
```

## ⚠️ Limitazioni Attuali

- Il parsing LDT è semplificato (no C-planes multiple)
- I DWG sono creati con ezdxf (non tutte le feature avanzate)
- I calcoli sono preliminari - verificare sempre con misurazioni reali
- La conversione da DWG a immagine ha limitazioni (esportare come JPG)

## 🔧 Configurazione Avanzata

### Aggiungere una Nuova Fotometria

1. Ottieni il file `.ldt` dal tuo fornitore di illuminazione
2. Carica tramite l'interfaccia "STEP 2"
3. Il sistema estrae automaticamente:
   - Nome prodotto
   - Flusso luminoso totale
   - Distribuzione intensità
   - Angoli caratteristici

### Personalizzare i Fattori di Calcolo

Modifica in `utils/lamp_calculator.py`:
```python
spacing = beam_width * 0.7  # Cambia da 0.7 a tuo fattore di sovrapposizione
```

## 🐛 Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| PDF non scarica | Verifica che `outputs/` sia scrivibile |
| DWG vuoto | Assicurati di aver disegnato almeno un'area |
| LDT non si carica | File corrotto o formato non supportato |
| Immagine PDF sfocata | Usa alta risoluzione (>150 DPI) |

## 📚 Documentazione Tecnica

- [Formato LDT (Eulumdat)](http://www.eulumdat.org/)
- [Calcoli Illuminotecnici - UNI EN 12464-1](https://www.uni.com)
- [EZDXF Documentation](https://ezdxf.readthedocs.io/)

## 🤝 Contributi

Le pull request sono benvenute! Per grandi cambiamenti, apri prima un issue.

## 📄 Licenza

MIT License - vedi file LICENSE per dettagli

## 👨‍💻 Autore

**LUXiA Development Team**
- Versione: 1.0
- Data: Gennaio 2026

---

**Nota**: Questo software è fornito per uso preliminare/concettuale. Per progetti professionali, verificare sempre i calcoli con software specializzato certificato e normativa locale.

Notes:
------
- The .ldt parser included is a simplified heuristic for MVP purposes. It attempts to find numeric blocks and guess
  intensity distributions, but it does not replace a full photometric engine. Use it for prototyping and validation;
  for professional work consider using certified photometric tools.
- Outputs (PDF reports) are saved in the outputs/ folder.
