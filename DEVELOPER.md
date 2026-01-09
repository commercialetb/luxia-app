# LUXiA - Documentazione Tecnica per Sviluppatori

## Architettura

```
luxia-app/
├── app.py                          # App principale Streamlit
├── config.py                       # Configurazione centralizzata
├── test_luxia.py                   # Test suite
├── setup.sh                        # Script setup
├── requirements.txt                # Dipendenze Python
├── README.md                       # Documentazione utente
├── GUIDA_RAPIDA.md                 # Quick start guide
├── CHANGELOG.md                    # Cronologia versioni
├── DEVELOPER.md                    # Questo file
├── .gitignore                      # Git ignore rules
├── outputs/                        # Cartella output (PDF/DWG)
└── utils/
    ├── photometry.py              # Parser LDT e calcoli beam
    ├── blueprint_processor.py      # Gestione planimetrie
    ├── lamp_calculator.py          # Calcoli lampade e DWG export
    └── report_generator.py         # Generazione PDF report
```

## Componenti Principali

### 1. app.py - Frontend Streamlit
**Responsabilità**:
- UI e interazione utente
- Gestione session state
- Flusso di lavoro a 4 step
- Orchestrazione dei moduli

**Librerie**:
- streamlit: Framework web
- PIL (Pillow): Elaborazione immagini
- numpy: Operazioni numeriche

### 2. photometry.py - Parser Fotometrie
**Funzioni principali**:
```python
parse_ldt(ldt_file) → dict
    Estrae dati da file Eulumdat
    Restituisce: name, intensities, total_luminous_flux, Imax

calculate_beam_spread(h, hc, angle_deg) → float
    Calcola larghezza fascio
    Formula: W = 2 × (h - hc) × tan(δ)

estimate_beam_angle_from_ldt(parsed) → float
    Stima angolo da dati LDT
    Heuristica: trova angle dove I(δ) ≈ 0.5 × Imax
```

**Limitazioni Note**:
- Parser LDT semplificato (non copre C-planes multiple)
- Estrazione flux usa euristica (cerca numero >100)
- Intensità estratte solo da primo array numerico

### 3. blueprint_processor.py - Gestione Planimetrie
**Classe BlueprintProcessor**:
```python
__init__(file_path, image)     # Carica immagine
resize_for_display(w, h)       # Ridimensiona per display
draw_areas(areas)              # Disegna aree su immagine
get_pil_image()                # Restituisce PIL Image

Funzioni esterne:
convert_pdf_to_image(pdf_file) # PDF → PIL Image
convert_dwg_to_image(dwg_file) # DWG → PIL Image (non impl.)
```

**Fallback**:
- Usa PIL come fallback quando OpenCV non disponibile
- Supporta sia cv2.rectangle che PIL.ImageDraw

### 4. lamp_calculator.py - Calcoli Lampade
**Classe LampPlacementCalculator**:
```python
calculate_spacing(width, height, beam_width) → dict
    Calcola:
    - total_lamps: numero lampade
    - lamps_x, lamps_y: griglia
    - spacing_x, spacing_y: spaziamento reale
    
    Algoritmo:
    spacing = beam_width × OVERLAP_FACTOR (default 0.7)
    n_x = ceil(width / spacing)
    n_y = ceil(height / spacing)

generate_lamp_positions(polygon, beam_width) → list[(x,y)]
    Genera coordinate lampade dentro poligono
    Usa point-in-polygon (ray casting)

export_to_dwg(filepath, areas_data) → str
    Crea file DWG con:
    - Layer "Areas": poligoni aree
    - Layer "Lamps": cerchi posizionamento
    - Layer "Grid": (futuro)
```

**Algoritmi**:
- Point-in-polygon: Ray casting algorithm
- Spacing: Distribuzione griglia uniforme

### 5. report_generator.py - Generazione PDF
**Classe ReportGenerator**:
```python
__init__(project_name, language)
generate_pdf(output_path, areas_data, total_lamps) → str
```

**Contenuto PDF**:
- Intestazione progetto
- Tabella riepilogativa aree
- Dettagli tecnici per area
- Note tecniche
- Dati fotometrie utilizzate

**Supporto Lingue**:
- Italiano (default)
- Inglese

## Flusso di Dati

```
┌─────────────────┐
│ Upload Files    │
├─────────────────┤
│ - Planimetria   │ → BlueprintProcessor
│ - Fotometrie    │ → parse_ldt()
└─────────────────┘
        ↓
┌─────────────────┐
│ User Input      │
├─────────────────┤
│ - Aree          │ → draw_areas()
│ - Parametri     │ → validate()
└─────────────────┘
        ↓
┌─────────────────┐
│ Calcoli         │
├─────────────────┤
│ - Fascio        │ → calculate_beam_spread()
│ - Lampade       │ → calculate_spacing()
│ - Posizioni     │ → generate_lamp_positions()
└─────────────────┘
        ↓
┌─────────────────┐
│ Output          │
├─────────────────┤
│ - PDF Report    │ → ReportGenerator.generate_pdf()
│ - DWG Layout    │ → export_to_dwg()
└─────────────────┘
```

## Session State

```python
st.session_state.blueprint        # BlueprintProcessor object
st.session_state.photometries     # dict[filename] → parsed LDT
st.session_state.areas            # list[dict] → area definitions
st.session_state.drawing_points   # list[(x,y)] → current drawing
st.session_state.current_drawing_mode  # 'rectangle' | 'polygon'
```

## Configurazione

File `config.py` centralizza:
```python
BEAM_OVERLAP_FACTOR = 0.7        # 30% sovrapposizione
DEFAULT_MOUNTING_HEIGHT = 3.0    # 3 metri
DEFAULT_CALC_PLANE_HEIGHT = 0.85 # 0.85 metri
MAX_IMAGE_WIDTH = 900            # pixel
DWG_LAMP_RADIUS = 0.1            # unità DWG
```

Modifica qui per personalizzare comportamento app.

## Estensioni Future

### 1. Editor Visuale Click-to-Draw
```python
# In app.py, step 3:
canvas = st.canvas(...)  # StreamlitCanvas
points = canvas.json_data['objects']
```

### 2. Import DWG con Layer Detection
```python
import ezdxf
doc = ezdxf.readfile('plan.dwg')
for layer in doc.layers:
    if layer.name == 'AREAS':
        # estrai entities
```

### 3. Calcoli Illuminotecnici Avanzati
```python
def calculate_uniformity_advanced(lamps, surfaces, irradiance_map):
    """Usa raytracing per uniformità reale"""
    # TODO: integra libreria raytracing
```

### 4. Database Fotometrie
```python
# Crea photometry_db.json con libreria standard
{
    "artemide_tolomeo": {"ldt": "...", "flux": 1000},
    "flos_2097": {"ldt": "...", "flux": 1500},
    ...
}
```

## Testing

### Unit Tests
```bash
python -m pytest tests/test_calculations.py -v
```

### Integration Tests
```bash
python test_luxia.py
```

### Manual Testing Checklist
- [ ] Upload JPG/PNG
- [ ] Upload PDF
- [ ] Upload LDT
- [ ] Draw area
- [ ] Calcola fascio
- [ ] Genera PDF
- [ ] Scarica DWG
- [ ] Prova con 2 aree diverse

## Performance Notes

### Limitazioni Attuali
- Max image resolution: 2000x2000 (limitazione Streamlit)
- Max areas: ~20 (UI responsiveness)
- Max photometries: ~10 (gestione memory)

### Ottimizzazioni Possibili
- Lazy loading immagini grandi
- Caching calcoli intermedi
- Compressione DWG
- Web worker per calcoli pesanti

## Troubleshooting Sviluppo

### ImportError cv2
→ OpenCV non disponibile in headless environments
→ Fallback a PIL implementato

### DWG Non Si Apre
→ Usa `ezdxf --validate file.dwg`
→ Prova con viewer online

### PDF Corrotto
→ Controlla encoding UTF-8 in testi
→ Verifica margini PDF validi

## Roadmap Tecnico

### v1.1 (Q1 2026)
- [ ] Click-to-draw editor
- [ ] DWG import con layer detection
- [ ] Cache calcoli persistente
- [ ] API REST basic
- [ ] Database SQLite fotometrie

### v1.2 (Q2 2026)
- [ ] 3D visualization (Three.js)
- [ ] PostgreSQL backend
- [ ] Auth utenti
- [ ] Cloud deployment (AWS/Azure)
- [ ] Mobile app React Native

### v2.0 (Q3 2026)
- [ ] Real raytracing (OptiX/Cycles)
- [ ] BRDF materials
- [ ] Time-series simulations
- [ ] Professional certification

## Contatti Sviluppatori

- **Repository**: https://github.com/yourusername/luxia-app
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: dev@luxia-app.com

## Licenza

MIT License - vedere LICENSE file

---

**Ultima modifica**: Gennaio 2026
**Versione**: 1.0
**Stato**: Stabile
