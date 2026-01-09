# LUXiA - Guida Rapida di Utilizzo

## 🎬 Avvio Rapido (5 minuti)

### 1️⃣ Preparazione File
Prima di avviare, assicurati di avere:
- **Planimetria** (formato JPG/PNG, consigliato 1200x800px)
- **File LDT** della tua lampada (fornito da produttore illuminazione)

### 2️⃣ Avvia l'App
```bash
streamlit run app.py
```
L'app si apre automaticamente su `http://localhost:8501`

### 3️⃣ Carica la Planimetria
- Sezione **STEP 1**
- Click su "Carica planimetria"
- Seleziona il tuo JPG/PNG

### 4️⃣ Carica la Fotometria
- Sezione **STEP 2**
- Click su "Carica fotometria LDT"
- Seleziona il file `.ldt` fornito dal produttore

### 5️⃣ Disegna le Aree
- Sezione **STEP 3**
- Immetti il **Nome Area** (es. "Zona Lettura")
- **Altezza Montaggio**: tipicamente 2.5-3.5m per uso residenziale
- **Altezza Piano Calcolo**: 0.85m = piano di lavoro standard
- **Seleziona Fotometria**: la lampada caricata al step 4
- Click **"Aggiungi Area"**

### 6️⃣ Visualizza i Risultati
- Sezione **STEP 4**
- Vedi automaticamente:
  - Larghezza fascio (m)
  - Numero lampade richieste
  - Spaziamento X e Y

### 7️⃣ Scarica i File
- **PDF Report**: riepilogo completo con tabelle
- **DWG Layout**: apri in AutoCAD per vedere il layout

---

## 📏 Conversione Distanze

Se lavori con misure diverse da metri:

| Da | A Metri | Formula |
|---|---------|---------|
| Centimetri | m | ÷ 100 |
| Millimetri | m | ÷ 1000 |
| Pollici | m | × 0.0254 |
| Piedi | m | × 0.3048 |

**Esempio**: Stanza di 400cm × 300cm = 4m × 3m

---

## 🔧 Parametri Tipici per Stanze

### Salotto
- **Altezza montaggio**: 2.7m
- **Piano calcolo**: 0.85m (piano dei sofà)
- **Angolo fascio**: 20-30° (fascio ampio)

### Cucina
- **Altezza montaggio**: 2.5m
- **Piano calcolo**: 0.9m (piano lavoro)
- **Angolo fascio**: 15-25° (più concentrato)

### Corridoio
- **Altezza montaggio**: 2.6m
- **Piano calcolo**: 0.0m (suolo)
- **Angolo fascio**: 30-40° (ampio)

### Ufficio
- **Altezza montaggio**: 3.0m
- **Piano calcolo**: 0.75m (piano scrivania)
- **Angolo fascio**: 15-20° (preciso)

---

## 📊 Interpretazione Risultati

### Larghezza Fascio (m)
Maggiore = fascio più ampio a terra
- Fascio **stretto** (< 3m): lampade spot, dettagli
- Fascio **medio** (3-6m): uso generale
- Fascio **ampio** (> 6m): ampi spazi

### Numero Lampade
Calcolato in base a:
$$\text{N. lampade} = \frac{\text{Area} \times 1.3}{\text{Area fascio}}$$

Fattore 1.3 = 30% sovrapposizione per uniformità

### Spaziamento (m)
Distanza tra lampade per copertura uniforme
- **X**: spaziamento orizzontale
- **Y**: spaziamento verticale

---

## 💡 Consigli Pratici

### 1. Scegli la Giusta Fotometria
- Chiedi al produttore il file LDT esatto del modello
- Verifica che corrisponda alla potenza/temperatura colore desiderata

### 2. Verifica l'Angolo
- Se LDT non è leggibile, usa questi valori tipici:
  - Spot: 15-20°
  - General lighting: 25-40°
  - Wide: 45-60°

### 3. Altezze Corrette
- **Montaggio**: misura dal soffitto al centro della lampada
- **Calcolo**: misura dal suolo al piano che vuoi illuminare

### 4. Sovrapposizione
- Uniformità migliore = più sovrapposizione = più lampade
- Il sistema calcola automaticamente con ~30% sovrapposizione

### 5. Verifiche di Realtà
- Risultati molto alti (>20 lampade/10m²)? Controlla parametri
- Risultati molto bassi? Potresti avere fotometria sbagliata

---

## 🚨 Problemi Comuni e Soluzioni

### "File LDT non si carica"
→ Verifica che sia un vero file Eulumdat (.ldt)
→ Apri con editor testo e verifica abbia dati numerici

### "PDF vuoto o numero lampade = 0"
→ Aggiungi almeno un'area (STEP 3)
→ Seleziona una fotometria caricata

### "DWG non si apre in AutoCAD"
→ Prova a rigenerare
→ Se persiste, converti a DXF nel suo CAD

### "Numero lampade sembra troppo alto/basso"
→ Verifica **altezza montaggio** (confusione m vs cm?)
→ Controlla **angolo fascio** (consultare datasheet lampada)

---

## 📖 Glossario Tecnico

| Termine | Significato |
|---------|------------|
| **Fotometria** | Caratteristiche di distribuzione luce di un apparecchio |
| **Fascio** | Cono di luce proiettato dalla lampada |
| **Angolo fascio (δ)** | Angolo di semiapertura del cono di luce (metà del cono totale) |
| **Eulumdat (.ldt)** | Formato standard internazionale per dati fotometrici |
| **Flusso luminoso (lm)** | Quantità totale di luce emessa (lumen) |
| **Illuminamento (lux)** | Luminosità su una superficie (lumen/m²) |
| **Uniformità** | Quanto bene la luce è distribuita in modo omogeneo |
| **Spaziamento** | Distanza tra lampade (passo) |

---

## 🔄 Workflow Completo - Esempio

**Scenario**: Illuminare salotto 5m × 4m, alt. soffitto 2.7m

```
1. Carica JPG planimetria salotto
2. Carica LDT lampada Artemide "Tolomeo" 
3. Disegna rettangolo area salotto:
   - Nome: "Salotto Principale"
   - H montaggio: 2.7m
   - H calcolo: 0.85m (sofà)
   - Fotometria: Artemide
   - Angolo: 25° (lettura datasheet)
4. Sistema calcola:
   - Larghezza fascio: ~2.9m
   - N. lampade: 6 (disposizione 2×3)
   - Spaziamento: 2.5m × 1.9m
5. Scarica PDF: vedi tabella riepilogativa
6. Scarica DWG: visualizza layout in CAD
```

---

## 📞 Supporto

Per problemi o domande:
1. Controlla glossario sopra
2. Leggi README.md completo
3. Verifica parametri con datasheet lampada

**Ricorda**: I calcoli sono preliminari. Verificare sempre con misurazioni e normativa locale!

---

**Ultima modifica**: Gennaio 2026
**Versione**: 1.0
