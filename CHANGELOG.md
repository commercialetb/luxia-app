# CHANGELOG - LUXiA

## [1.0.0] - 2026-01-09

### 🎉 Rilascio Iniziale

#### ✨ Caratteristiche Principali
- **Caricamento Planimetrie**: Supporto JPG, PNG, PDF, DWG
- **Gestione Fotometrie**: Upload file LDT (Eulumdat) con parsing automatico
- **Disegno Aree**: Interfaccia visuale per selezionare rettangoli/poligoni
- **Calcoli Illuminotecnici**:
  - Calcolo larghezza fascio in base a altezza e angolo
  - Stima automatica numero lampade
  - Calcolo spaziamento ottimale per uniformità
- **Generazione Report PDF**: Riepilogo con tabelle aree, prodotti, quantità
- **Export DWG**: File AutoCAD con aree e posizionamento lampade
- **Interfaccia Bilingue**: Italiano e Inglese

#### 📦 Dipendenze Principale
- Streamlit 1.28+
- FPDF2 per generazione PDF
- EZDXF per creazione DWG
- Pillow per elaborazione immagini
- OpenCV per visione artificiale (opzionale)

#### 🐛 Problemi Noti
- Parsing LDT semplificato (no C-planes multiple)
- DWG creati con ezdxf (feature avanzate non supportate)
- Calcoli sono preliminari - verificare sempre con software certificato
- Conversione DWG→Immagine ha limitazioni (esportare come JPG)

#### 🔒 Requisiti Sistema
- Python 3.8+
- ~500MB spazio disco
- Memoria RAM: 2GB minimo, 4GB consigliato

#### 📝 Documentazione
- README.md: Documentazione completa
- GUIDA_RAPIDA.md: Quick start guide
- config.py: Configurazione centralizzata
- test_luxia.py: Test suite automatico

---

## [1.1.0] - Pianificato

### Previsto
- [ ] Editor visuale planimetrie (click per disegnare)
- [ ] Importazione DWG con layer detection
- [ ] Calcoli illuminotecnici avanzati (uniformità reale)
- [ ] Libreria fotometrie precaricate
- [ ] Export XLSX (Excel) con dettagli
- [ ] Calcolo consumi energetici
- [ ] Simulazione 3D preliminare
- [ ] Gestione progetti (salva/carica)
- [ ] API REST per integrazione

---

## [1.2.0] - Pianificato

### Previsto
- [ ] Supporto multi-lingue esteso (Spagnolo, Francese, Tedesco)
- [ ] Database fotometrie (IES, Eulumdat)
- [ ] Calcoli UNI EN 12464 completi
- [ ] Rendering 3D avanzato
- [ ] Cloud storage integrato
- [ ] Mobile app nativa
- [ ] Collaborazione in tempo reale

---

## Cronologia Versioni

| Versione | Data | Stato |
|----------|------|-------|
| 1.0.0 | 2026-01-09 | ✅ Stabile |
| 1.1.0 | TBD | 🔄 Pianificato |
| 1.2.0 | TBD | 🔄 Pianificato |

---

## Note di Rilascio

### Per Sviluppatori

Per aggiornare le versioni, modificare:
1. `config.py`: `APP_VERSION`
2. `config.py`: `BUILD_DATE`
3. Questo file: aggiungere entrata nel changelog

### Processo di Release
```bash
# 1. Testa tutto
python test_luxia.py

# 2. Aggiorna CHANGELOG
# 3. Tag commit
git tag -a v1.0.0 -m "Release 1.0.0"

# 4. Push
git push origin v1.0.0
```

---

## Ringraziamenti

Sviluppato con ❤️ usando:
- Streamlit
- FPDF2
- EZDXF
- Pillow
- NumPy

---

**Licenza**: MIT
**Autore**: LUXiA Development Team
**Website**: https://github.com/yourusername/luxia-app
