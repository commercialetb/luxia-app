LUXiA - Light Analysis & Calculation App (MVP)
=================================================

This package contains a Streamlit-based MVP for LUXiA — a tool to analyze Eulumdat (.ldt)
photometric files, compute beam spread on a chosen calculation plane, estimate number of luminaires
and a simple uniformity metric. The package is bilingual (Italian / English).

How to run (local):
-------------------
1. Install Python 3.8+
2. Open terminal and go to the project folder
3. Create a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate   (Linux / Mac)
   venv\Scripts\activate      (Windows)
4. Install dependencies:
   pip install -r requirements.txt
5. Run the app:
   streamlit run app.py
6. The app will open in your browser at http://localhost:8501

Notes:
------
- The .ldt parser included is a simplified heuristic for MVP purposes. It attempts to find numeric blocks and guess
  intensity distributions, but it does not replace a full photometric engine. Use it for prototyping and validation;
  for professional work consider using certified photometric tools.
- Outputs (PDF reports) are saved in the outputs/ folder.
