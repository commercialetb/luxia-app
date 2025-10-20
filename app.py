import streamlit as st
import math, io, os
from datetime import datetime
from fpdf import FPDF
from PIL import Image
from utils.photometry import parse_ldt, calculate_beam_spread, estimate_beam_angle_from_ldt

# --- Translations ---
TRANSLATIONS = {
    "it": {
        "title": "💡 LUXiA – Analisi e Calcolo Illuminotecnico",
        "description": "Analizza fotometrie, calcola fasci luminosi e uniformità dai file .LDT.",
        "lang_label": "Lingua",
        "upload_label": "Carica file fotometrico (.LDT)",
        "project": "Progetto",
        "add_room": "Aggiungi ambiente",
        "room_name": "Nome ambiente",
        "room_height": "Altezza installazione lampada (m)",
        "calc_plane": "Altezza piano di calcolo (m)",
        "angle_label": "Angolo (semiapertura) δ (°) - se non disponibile, seleziona 'Auto'",
        "auto": "Auto (da .LDT)",
        "manual": "Manuale",
        "calc_button": "Calcola fascio e quantità",
        "beam_width": "Larghezza del fascio sul piano di calcolo",
        "beam_area": "Area del fascio",
        "n_lamps": "Numero stimato di lampade",
        "uniformity": "Uniformità stimata",
        "download_pdf": "Scarica report PDF",
        "no_ldt": "Nessun file .LDT caricato o parsing non riuscito: inserire angolo manualmente.",
        "info": "Nota: il parsing .LDT è semplificato. Per risultati professionali utilizzare fotometrie standard e verificare i risultati.",
    },
    "en": {
        "title": "💡 LUXiA – Light Analysis & Calculation App",
        "description": "Analyze photometric files, compute beam spread and uniformity from .LDT data.",
        "lang_label": "Language",
        "upload_label": "Upload photometric file (.LDT)",
        "project": "Project",
        "add_room": "Add room",
        "room_name": "Room name",
        "room_height": "Luminaire mounting height (m)",
        "calc_plane": "Calculation plane height (m)",
        "angle_label": "Beam semi-angle δ (°) - if not available choose 'Auto'",
        "auto": "Auto (from .LDT)",
        "manual": "Manual",
        "calc_button": "Compute beam & quantities",
        "beam_width": "Beam width on calculation plane",
        "beam_area": "Beam area",
        "n_lamps": "Estimated number of luminaires",
        "uniformity": "Estimated uniformity",
        "download_pdf": "Download PDF report",
        "no_ldt": "No .LDT file uploaded or parsing failed: please enter angle manually.",
        "info": "Note: .LDT parsing is simplified. For professional results use standard photometries and verify outputs.",
    }
}

st.set_page_config(page_title="LUXiA", layout="wide")

# --- Sidebar / settings ---
lang = st.sidebar.radio("Lingua / Language", ("🇮🇹 Italiano", "🇬🇧 English"))
lang_code = "it" if lang.startswith("🇮🇹") else "en"
T = TRANSLATIONS[lang_code]

st.title(T["title"])
st.write(T["description"])
st.markdown("---")

# Project parameters
st.sidebar.header(T["project"])
project_name = st.sidebar.text_input("Project name", "LUXiA Demo Project")
st.sidebar.markdown("### Rooms / Ambienti")
n_rooms = st.sidebar.number_input("Number of rooms", min_value=1, max_value=12, value=1, step=1)

# Upload LDT
st.subheader(T["upload_label"])
ldt_file = st.file_uploader(T["upload_label"], type=["ldt", "LDT"])
parsed = None
if ldt_file is not None:
    try:
        parsed = parse_ldt(ldt_file)
        st.success(f"Loaded: {parsed.get('name','<unknown>')}")
    except Exception as e:
        st.error("Error parsing .LDT: " + str(e))
        parsed = None

st.info(T["info"])
st.markdown("---")

# For each room, collect parameters and compute
rooms = []
for i in range(int(n_rooms)):
    st.header(f"{T['project']} - {i+1}")
    cols = st.columns(3)
    room_name = cols[0].text_input(T["room_name"], value=f"Room_{i+1}", key=f"name_{i}")
    h = cols[1].number_input(T["room_height"], min_value=0.5, max_value=20.0, value=3.0, key=f"h_{i}")
    hc = cols[2].number_input(T["calc_plane"], min_value=0.0, max_value=5.0, value=0.85, key=f"hc_{i}")

    st.markdown("**Angle selection / Selezione angolo**")
    angle_mode = st.radio("", (T["auto"], T["manual"]), index=0 if parsed else 1, key=f"amode_{i}")
    angle_deg = None
    if angle_mode == T["auto"] and parsed:
        try:
            angle_deg = estimate_beam_angle_from_ldt(parsed)
            st.write(f"Auto-estimated semi-angle δ = {angle_deg:.1f}° (from .LDT)")
        except Exception as e:
            st.warning(T["no_ldt"])
            angle_mode = T["manual"]
    if angle_mode == T["manual"] or angle_deg is None:
        angle_deg = st.slider(T["angle_label"], min_value=1.0, max_value=90.0, value=15.0, key=f"angle_{i}")

    surface = st.number_input("Surface area (m²) / Superficie (m²)", min_value=1.0, max_value=10000.0, value=30.0, key=f"area_{i}")

    # Compute beam and estimates
    if st.button(T["calc_button"], key=f"calc_{i}"):
        beam_width = calculate_beam_spread(h, hc, angle_deg)
        radius = beam_width/2.0
        beam_area = math.pi * (radius**2)
        n_lamps = math.ceil(surface / beam_area)
        coverage = (n_lamps * beam_area) / surface
        uniformity = min(coverage, 1.0)

        st.write(f"**{T['beam_width']}:** {beam_width:.2f} m")
        st.write(f"**{T['beam_area']}:** {beam_area:.2f} m²")
        st.write(f"**{T['n_lamps']}:** {n_lamps}")
        st.write(f"**{T['uniformity']}:** {uniformity*100:.1f} %")

        # If parsed LDT has lumen, show illuminance estimate (very simplified)
        if parsed and parsed.get('total_luminous_flux'):
            flux = parsed['total_luminous_flux']
            # assume portion of flux within main cone approx = 0.7 (simplified)
            flux_eff = flux * 0.7
            E_mean = flux_eff / (n_lamps * beam_area)
            st.write(f"Estimated average illuminance per lamp (simplified): {E_mean:.1f} lx")

        # Generate PDF report
        if st.button(T["download_pdf"], key=f"pdf_{i}"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"LUXiA Report: {project_name}", ln=True)
            pdf.set_font("Helvetica", size=11)
            pdf.cell(0, 8, f"Room: {room_name}", ln=True)
            pdf.cell(0, 8, f"Mounting height h: {h} m, Calc plane hc: {hc} m", ln=True)
            pdf.cell(0, 8, f"Semi-angle δ: {angle_deg:.1f}°", ln=True)
            pdf.cell(0, 8, f"Beam width: {beam_width:.2f} m", ln=True)
            pdf.cell(0, 8, f"Beam area: {beam_area:.2f} m²", ln=True)
            pdf.cell(0, 8, f"Number of luminaires: {n_lamps}", ln=True)
            pdf.cell(0, 8, f"Estimated uniformity: {uniformity*100:.1f} %", ln=True)
            if parsed and parsed.get('total_luminous_flux'):
                pdf.cell(0, 8, f"Photometry source: {parsed.get('name','n/a')}", ln=True)
                pdf.cell(0, 8, f"Total luminous flux (lm): {parsed.get('total_luminous_flux')}", ln=True)
            out_name = os.path.join("outputs", f"{project_name.replace(' ','_')}_{room_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
            pdf.output(out_name)
            with open(out_name, "rb") as f:
                st.download_button(T["download_pdf"], f, file_name=os.path.basename(out_name), mime="application/pdf")
