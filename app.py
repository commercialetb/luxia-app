import streamlit as st
import math
import io
import os
import json
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw
from pathlib import Path

# Import utility modules
from utils.photometry import parse_ldt, calculate_beam_spread, estimate_beam_angle_from_ldt
from utils.blueprint_processor import BlueprintProcessor, convert_pdf_to_image
from utils.lamp_calculator import LampPlacementCalculator
from utils.report_generator import ReportGenerator

# Try to import drawable canvas
try:
    from streamlit_drawable_canvas import st_canvas
    HAS_CANVAS = True
except Exception:
    HAS_CANVAS = False

# ============================================================================
# TRADUZIONI
# ============================================================================
TRANSLATIONS = {
    "it": {
        "title": "💡 LUXiA – Progettazione Illuminotecnica Avanzata",
        "description": "Carica planimetrie, seleziona aree, posiziona fotometrie e calcola quantità lampade",
        "lang": "Lingua",
        "step1": "STEP 1: Carica Planimetria",
        "step2": "STEP 2: Seleziona Fotometrie",
        "step3": "STEP 3: Disegna Aree",
        "step4": "STEP 4: Calcoli e Export",
        "upload_blueprint": "Carica planimetria (JPG, PNG, PDF, DWG)",
        "file_uploaded": "Planimetria caricata ✓",
        "upload_photometry": "Carica fotometria LDT",
        "photometry_uploaded": "Fotometria caricata ✓",
        "project_name": "Nome Progetto",
        "drawing_mode": "Modalità Disegno",
        "mode_rectangle": "Rettangolo",
        "mode_polygon": "Poligono",
        "clear_drawing": "Cancella Ultimo",
        "add_area": "Aggiungi Area",
        "area_added": "Area aggiunta ✓",
        "area_name": "Nome Area",
        "height_mounting": "Altezza Montaggio (m)",
        "height_calc_plane": "Altezza Piano Calcolo (m)",
        "select_photometry": "Seleziona Fotometria",
        "beam_angle": "Angolo Fascio (°)",
        "auto": "Auto da LDT",
        "manual": "Manuale",
        "calculate": "Calcola Lampade",
        "beam_width": "Larghezza Fascio",
        "spacing_info": "Spaziamento (m)",
        "lamps_needed": "Lampade Necessarie",
        "download_pdf": "⬇️ Scarica PDF Report",
        "download_dwg": "⬇️ Scarica DWG Layout",
        "no_blueprint": "Carica una planimetria per iniziare",
        "no_areas": "Nessuna area disegnata ancora",
        "summary": "Riepilogo Progetto",
        "total_lamps": "Lampade Totali",
        "total_area": "Superficie Totale",
    },
    "en": {
        "title": "💡 LUXiA – Advanced Lighting Design",
        "description": "Upload floorplan, select areas, place photometries and calculate lamp quantities",
        "lang": "Language",
        "step1": "STEP 1: Upload Floorplan",
        "step2": "STEP 2: Select Photometries",
        "step3": "STEP 3: Draw Areas",
        "step4": "STEP 4: Calculate & Export",
        "upload_blueprint": "Upload floorplan (JPG, PNG, PDF, DWG)",
        "file_uploaded": "Floorplan uploaded ✓",
        "upload_photometry": "Upload LDT photometry",
        "photometry_uploaded": "Photometry uploaded ✓",
        "project_name": "Project Name",
        "drawing_mode": "Drawing Mode",
        "mode_rectangle": "Rectangle",
        "mode_polygon": "Polygon",
        "clear_drawing": "Clear Last",
        "add_area": "Add Area",
        "area_added": "Area added ✓",
        "area_name": "Area Name",
        "height_mounting": "Mounting Height (m)",
        "height_calc_plane": "Calculation Plane Height (m)",
        "select_photometry": "Select Photometry",
        "beam_angle": "Beam Angle (°)",
        "auto": "Auto from LDT",
        "manual": "Manual",
        "calculate": "Calculate Lamps",
        "beam_width": "Beam Width",
        "spacing_info": "Spacing (m)",
        "lamps_needed": "Lamps Needed",
        "download_pdf": "⬇️ Download PDF Report",
        "download_dwg": "⬇️ Download DWG Layout",
        "no_blueprint": "Upload a floorplan to start",
        "no_areas": "No areas drawn yet",
        "summary": "Project Summary",
        "total_lamps": "Total Lamps",
        "total_area": "Total Area",
    }
}

# ============================================================================
# CONFIGURAZIONE STREAMLIT
# ============================================================================
st.set_page_config(page_title="LUXiA", layout="wide", initial_sidebar_state="expanded")

# Lingua
lang = st.sidebar.radio("🌍", ("🇮🇹 Italiano", "🇬🇧 English"), label_visibility="collapsed")
lang_code = "it" if lang.startswith("🇮🇹") else "en"
T = TRANSLATIONS[lang_code]

st.title(T["title"])
st.write(T["description"])
st.markdown("---")

# Crea cartella output
os.makedirs("outputs", exist_ok=True)

# ============================================================================
# INIZIALIZZA SESSION STATE
# ============================================================================
if 'blueprint' not in st.session_state:
    st.session_state.blueprint = None
if 'photometries' not in st.session_state:
    st.session_state.photometries = {}
if 'areas' not in st.session_state:
    st.session_state.areas = []
if 'drawing_points' not in st.session_state:
    st.session_state.drawing_points = []
if 'current_drawing_mode' not in st.session_state:
    st.session_state.current_drawing_mode = 'rectangle'

# ============================================================================
# STEP 1: CARICA PLANIMETRIA
# ============================================================================
st.header(f"📐 {T['step1']}")
blueprint_file = st.file_uploader(T['upload_blueprint'], type=['jpg', 'jpeg', 'png', 'pdf', 'dwg'])

if blueprint_file:
    file_ext = blueprint_file.name.split('.')[-1].lower()
    
    if file_ext == 'pdf':
        image = convert_pdf_to_image(blueprint_file)
        if image:
            st.session_state.blueprint = BlueprintProcessor(image=image)
            st.success(T['file_uploaded'])
    elif file_ext in ['jpg', 'jpeg', 'png']:
        image = Image.open(blueprint_file)
        st.session_state.blueprint = BlueprintProcessor(image=image)
        st.success(T['file_uploaded'])
    elif file_ext == 'dwg':
        st.info("DWG support: si consiglia di esportare come JPG/PNG")

if st.session_state.blueprint:
    st.session_state.blueprint.resize_for_display(max_width=800, max_height=600)

# ============================================================================
# STEP 2: CARICA FOTOMETRIE
# ============================================================================
st.header(f"💡 {T['step2']}")
col1, col2 = st.columns(2)

with col1:
    ldt_file = st.file_uploader(T['upload_photometry'], type=['ldt'], key='ldt_upload')
    if ldt_file:
        try:
            photometry = parse_ldt(ldt_file)
            photom_name = photometry.get('name', 'Unknown').strip()[:30]
            st.session_state.photometries[ldt_file.name] = photometry
            st.success(f"{T['photometry_uploaded']}: {photom_name}")
        except Exception as e:
            st.error(f"Errore parsing LDT: {str(e)}")

with col2:
    if st.session_state.photometries:
        st.info(f"📦 {len(st.session_state.photometries)} fotometria/e caricata/e")

# ============================================================================
# STEP 3: DISEGNA AREE SULLA PLANIMETRIA
# ============================================================================
st.header(f"✏️ {T['step3']}")

if not st.session_state.blueprint:
    st.warning(T['no_blueprint'])
else:
    col_left, col_right = st.columns([2, 1])
    
    with col_right:
        st.subheader("⚙️ Opzioni")
        
        project_name = st.text_input(T['project_name'], "LUXiA_Project")
        
        st.markdown("**Modalità Disegno**")
        drawing_mode = st.radio(
            T['drawing_mode'],
            [T['mode_rectangle'], T['mode_polygon']],
            label_visibility="collapsed"
        )
        st.session_state.current_drawing_mode = 'rectangle' if drawing_mode == T['mode_rectangle'] else 'polygon'
        
        if st.button("🗑️ " + T['clear_drawing'], use_container_width=True):
            st.session_state.drawing_points = []
            st.rerun()
        
        st.divider()
        st.subheader("📊 Aree Disegnate")
        for idx, area in enumerate(st.session_state.areas):
            st.write(f"✓ {area['name']} - {len(area['points'])} punti")
        # Scala immagine / Riferimento
        st.markdown("**Scala immagine / Riferimento**")
        if 'pixels_per_meter' not in st.session_state:
            st.session_state.pixels_per_meter = None
        if HAS_CANVAS:
            ref_mode = st.radio("Imposta riferimento", ("Disegna Linea", "Manuale"), index=0)
            if ref_mode == "Disegna Linea":
                st.info("Disegna una linea di riferimento sulla planimetria e inserisci la lunghezza reale.")
        else:
            st.info("Canvas non disponibile: usa input manuale per scala")
    
    with col_left:
        # Mostra blueprint con aree
        if st.session_state.areas:
            display_img = st.session_state.blueprint.draw_areas(st.session_state.areas)
        else:
            display_img = st.session_state.blueprint.get_pil_image()

        # Canvas drawing support (optional)
        if HAS_CANVAS:
            pil_img = display_img.convert('RGB') if hasattr(display_img, 'convert') else display_img
            bg_width, bg_height = pil_img.size
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#ff0000",
                background_image=pil_img,
                update_streamlit=True,
                height=min(800, bg_height),
                width=min(1200, bg_width),
                drawing_mode="rect",
                key="canvas_areas",
            )

            # Reference line canvas for scale (if scale not set)
            if st.session_state.get('pixels_per_meter', None) is None:
                st.markdown("#### Imposta Scala (se non presente)")
                st.write("Disegna una linea (tool linea) e poi inserisci la lunghezza reale in metri.")
                ref_canvas = st_canvas(
                    fill_color=None,
                    stroke_width=2,
                    stroke_color="#00ff00",
                    background_image=pil_img,
                    update_streamlit=True,
                    height=min(800, bg_height),
                    width=min(1200, bg_width),
                    drawing_mode="line",
                    key="canvas_ref",
                )
                if ref_canvas and getattr(ref_canvas, 'json_data', None) and 'objects' in ref_canvas.json_data and len(ref_canvas.json_data['objects'])>0:
                    obj = ref_canvas.json_data['objects'][-1]
                    px_length = None
                    if obj.get('type') == 'line':
                        x1 = obj.get('x1') if obj.get('x1') is not None else obj.get('left', 0)
                        y1 = obj.get('y1') if obj.get('y1') is not None else obj.get('top', 0)
                        x2 = obj.get('x2') if obj.get('x2') is not None else (obj.get('left', 0) + obj.get('width', 0))
                        y2 = obj.get('y2') if obj.get('y2') is not None else (obj.get('top', 0) + obj.get('height', 0))
                        try:
                            px_length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
                        except Exception:
                            px_length = None
                    if px_length:
                        real_len = st.number_input("Lunghezza reale della linea (m)", min_value=0.01, value=1.0, step=0.01)
                        if st.button("Imposta Scala (pixels/m)"):
                            st.session_state.pixels_per_meter = px_length / float(real_len)
                            st.success(f"Scala impostata: {st.session_state.pixels_per_meter:.2f} px/m")

            # Process drawn rectangles as new areas (only when new objects appear)
            if canvas_result and getattr(canvas_result, 'json_data', None) and 'objects' in canvas_result.json_data:
                objs = canvas_result.json_data['objects']
                last_count = st.session_state.get('canvas_last_count', 0)
                if len(objs) > last_count:
                    # process only the new objects
                    for obj in objs[last_count:]:
                        otype = obj.get('type') or obj.get('shape') or ''
                        pts = None
                        # Rect
                        if otype == 'rect' or obj.get('width') is not None:
                            left = obj.get('left', 0)
                            top = obj.get('top', 0)
                            width = obj.get('width', 0)
                            height = obj.get('height', 0)
                            pts = [(left, top), (left+width, top+height)]
                            area_type = 'rectangle'
                        # Line -> ignore as area
                        elif otype == 'line':
                            pts = None
                        # Polygon / Polyline
                        elif 'points' in obj and isinstance(obj['points'], list):
                            # fabric.js may store points as list of dicts
                            try:
                                pts = [(p['x'], p['y']) if isinstance(p, dict) else (p[0], p[1]) for p in obj['points']]
                                area_type = 'polygon'
                            except Exception:
                                pts = None
                        # Path (freehand) -> extract coords from path commands
                        elif 'path' in obj and isinstance(obj['path'], list):
                            coords = []
                            try:
                                for cmd in obj['path']:
                                    # cmd like ['M', x, y] or ['L', x, y]
                                    if len(cmd) >= 3 and isinstance(cmd[1], (int, float)):
                                        coords.append((cmd[1], cmd[2]))
                                if len(coords) >= 2:
                                    pts = coords
                                    area_type = 'polygon'
                            except Exception:
                                pts = None
                        # If we have points, store them (they are in display coords)
                        if pts:
                            a_name = f"Area_{len(st.session_state.areas)+1}"
                            # compute approximate area in pixels (shoelace) and convert to m2 if scale present
                            def polygon_area_px(points):
                                x = [p[0] for p in points]
                                y = [p[1] for p in points]
                                n = len(points)
                                area = 0.0
                                for i in range(n):
                                    j = (i + 1) % n
                                    area += x[i] * y[j] - x[j] * y[i]
                                return abs(area) / 2.0

                            area_px = polygon_area_px(pts) if len(pts) >= 3 else abs((pts[1][0]-pts[0][0])*(pts[1][1]-pts[0][1]))
                            ppm = st.session_state.get('pixels_per_meter', None)
                            surface_m2 = None
                            if ppm and ppm > 0:
                                surface_m2 = area_px / (ppm**2)

                            new_area = {
                                'name': a_name,
                                'points': pts,
                                'type': area_type if 'area_type' in locals() else 'polygon',
                                'height_mounting': 3.0,
                                'height_calc_plane': 0.85,
                                'photometry': '<Manual>',
                                'surface_m2': surface_m2,
                            }
                            st.session_state.areas.append(new_area)
                    st.session_state.canvas_last_count = len(objs)
                    st.success(f"Aggiunte {len(objs) - last_count} area/e dal canvas")

        # Mostra immagine (fallback)
        st.image(display_img, use_column_width=True)
        
        # Inserimento area manuale
        st.markdown("### Inserisci Area Manualmente")
        col_an, col_ah1, col_ah2 = st.columns(3)
        with col_an:
            area_name = st.text_input(T['area_name'], f"Area_{len(st.session_state.areas)+1}", key=f"area_name_{len(st.session_state.areas)}")
        with col_ah1:
            height_m = st.number_input(T['height_mounting'], 2.5, 10.0, 3.0, 0.1, key=f"height_m_{len(st.session_state.areas)}")
        with col_ah2:
            height_c = st.number_input(T['height_calc_plane'], 0.0, 3.0, 0.85, 0.1, key=f"height_c_{len(st.session_state.areas)}")
        
        col_photo, col_btn = st.columns([2, 1])
        with col_photo:
            selected_photom = st.selectbox(
                T['select_photometry'],
                list(st.session_state.photometries.keys()) + ["<Manual>"],
                key=f"photom_select_{len(st.session_state.areas)}"
            )
        
        with col_btn:
            if st.button(T['add_area'], use_container_width=True):
                if area_name.strip():
                    start_idx = len(st.session_state.areas)
                    new_area = {
                        'name': area_name,
                        'points': [(100 + start_idx*20, 100 + start_idx*20), (200 + start_idx*20, 200 + start_idx*20)],  # Default rectangle
                        'type': 'rectangle',
                        'height_mounting': height_m,
                        'height_calc_plane': height_c,
                        'photometry': selected_photom,
                    }
                    st.session_state.areas.append(new_area)
                    st.success(T['area_added'])
                    st.rerun()

# ============================================================================
# STEP 4: CALCOLI E EXPORT
# ============================================================================
st.header(f"📊 {T['step4']}")

if st.session_state.areas and st.session_state.photometries:
    
    areas_data = []
    total_lamps = 0
    total_area = 0
    
    for area_idx, area in enumerate(st.session_state.areas):
        st.subheader(f"🎯 {area['name']}")
        
        col1, col2, col3 = st.columns(3)
        
        # Carica fotometria
        photom = st.session_state.photometries.get(area['photometry'], {})
        
        # Calcoli
        with col1:
            st.metric("Altezza Montaggio", f"{area['height_mounting']:.2f} m")
        
        with col2:
            st.metric("Altezza Piano Calcolo", f"{area['height_calc_plane']:.2f} m")
        
        with col3:
            beam_angle = st.number_input(
                T['beam_angle'],
                1, 90, 15,
                key=f"beam_angle_{area_idx}"
            )
        
        # Calcola fascio
        height_diff = area['height_mounting'] - area['height_calc_plane']
        beam_width = calculate_beam_spread(area['height_mounting'], area['height_calc_plane'], beam_angle)
        beam_area = math.pi * (beam_width/2)**2
        # Area superficie
        surface_area = None
        # If area has precomputed surface in m2 (from canvas), use it
        if area.get('surface_m2'):
            surface_area = area['surface_m2']
        else:
            # try to compute from polygon points if possible using pixels_per_meter
            pts = area.get('points', [])
            if pts and len(pts) >= 2:
                # compute pixel area (shoelace for polygons or rectangle)
                def polygon_area_px(points):
                    x = [p[0] for p in points]
                    y = [p[1] for p in points]
                    n = len(points)
                    area_px = 0.0
                    for i in range(n):
                        j = (i + 1) % n
                        area_px += x[i] * y[j] - x[j] * y[i]
                    return abs(area_px) / 2.0

                if len(pts) >= 3:
                    area_px = polygon_area_px(pts)
                else:
                    # rectangle defined by two points
                    area_px = abs((pts[1][0]-pts[0][0])*(pts[1][1]-pts[0][1]))

                ppm = st.session_state.get('pixels_per_meter', None)
                if ppm and ppm > 0:
                    surface_area = area_px / (ppm**2)
                else:
                    # fallback: assume 1 px = 1 m (not ideal)
                    surface_area = area_px
        if surface_area is None:
            surface_area = 0
        
        # Calcola numero lampade
        calc = LampPlacementCalculator(photom)
        spacing_config = calc.calculate_spacing(10, 10, beam_width)  # 10x10m area default
        
        n_lamps = spacing_config['total_lamps']
        spacing_x = spacing_config['spacing_x']
        spacing_y = spacing_config['spacing_y']
        
        total_lamps += n_lamps
        total_area += surface_area
        
        col_col1, col_col2, col_col3 = st.columns(3)
        with col_col1:
            st.metric(T['beam_width'], f"{beam_width:.2f} m")
        with col_col2:
            st.metric(T['lamps_needed'], n_lamps)
        with col_col3:
            st.metric("Uniformità", "95%")
        
        st.write(f"📏 Spaziamento: X={spacing_x:.2f}m, Y={spacing_y:.2f}m")
        
        areas_data.append({
            'name': area['name'],
            'surface': surface_area,
            'lamps': n_lamps,
            'beam_width': beam_width,
            'spacing_x': spacing_x,
            'spacing_y': spacing_y,
            'height': area['height_mounting'],
            'uniformity': 95.0,
            'photometry_name': area['photometry'],
            'points': area['points'],
            'lamp_positions': [(50+i*spacing_x, 50+j*spacing_y) for i in range(spacing_config['lamps_x']) for j in range(spacing_config['lamps_y'])],
        })
        
        st.divider()
    
    # ========================================================================
    # RIEPILOGO FINALE
    # ========================================================================
    st.subheader(f"📋 {T['summary']}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(T['total_lamps'], total_lamps)
    with col2:
        st.metric(T['total_area'], f"{total_area:.2f} m²")
    with col3:
        st.metric("N. Aree", len(st.session_state.areas))
    
    # ========================================================================
    # DOWNLOAD PDF
    # ========================================================================
    report_gen = ReportGenerator(project_name, lang_code)
    pdf_path = f"outputs/{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_gen.generate_pdf(pdf_path, areas_data, total_lamps)
    
    with open(pdf_path, 'rb') as f:
        st.download_button(
            label=T['download_pdf'],
            data=f.read(),
            file_name=os.path.basename(pdf_path),
            mime='application/pdf'
        )
    
    # ========================================================================
    # DOWNLOAD DWG
    # ========================================================================
    dwg_path = f"outputs/{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dwg"
    calc = LampPlacementCalculator()
    calc.export_to_dwg(dwg_path, areas_data)
    
    with open(dwg_path, 'rb') as f:
        st.download_button(
            label=T['download_dwg'],
            data=f.read(),
            file_name=os.path.basename(dwg_path),
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

else:
    st.info("⏳ Completare i step precedenti per accedere ai calcoli")

st.markdown("---")
st.caption("LUXiA v1.0 - Progettazione illuminotecnica avanzata")
