from fpdf import FPDF
from datetime import datetime
import os

class ReportGenerator:
    """Genera report PDF completo con riepilogo aree, prodotti e quantità"""
    
    def __init__(self, project_name, language='it'):
        self.project_name = project_name
        self.language = language
        self.timestamp = datetime.now()
        
        # Testi in italiano e inglese
        self.texts = {
            'it': {
                'title': 'LUXiA - Report Progetto Illuminotecnico',
                'project': 'Progetto',
                'date': 'Data',
                'summary': 'RIEPILOGO PROGETTO',
                'areas': 'Aree Analizzate',
                'products': 'Prodotti Utilizzati',
                'area_name': 'Nome Area',
                'area_size': 'Superficie (m²)',
                'photometry': 'Fotometria',
                'beam_width': 'Larghezza Fascio (m)',
                'mounting_height': 'Altezza Montaggio (m)',
                'lamps_required': 'Lampade Necessarie',
                'spacing_x': 'Passo X (m)',
                'spacing_y': 'Passo Y (m)',
                'estimated_illuminance': 'Illuminamento Est. (lux)',
                'product_code': 'Codice Prodotto',
                'quantity': 'Quantità',
                'total': 'TOTALE LAMPADE',
                'notes': 'Note Tecniche',
                'uniformity': 'Uniformità (%)',
            },
            'en': {
                'title': 'LUXiA - Lighting Design Report',
                'project': 'Project',
                'date': 'Date',
                'summary': 'PROJECT SUMMARY',
                'areas': 'Analyzed Areas',
                'products': 'Products Used',
                'area_name': 'Area Name',
                'area_size': 'Surface (m²)',
                'photometry': 'Photometry',
                'beam_width': 'Beam Width (m)',
                'mounting_height': 'Mounting Height (m)',
                'lamps_required': 'Lamps Required',
                'spacing_x': 'Spacing X (m)',
                'spacing_y': 'Spacing Y (m)',
                'estimated_illuminance': 'Est. Illuminance (lux)',
                'product_code': 'Product Code',
                'quantity': 'Quantity',
                'total': 'TOTAL LAMPS',
                'notes': 'Technical Notes',
                'uniformity': 'Uniformity (%)',
            }
        }
        self.t = self.texts[language]
    
    def generate_pdf(self, output_path, areas_data, total_lamps):
        """
        Genera PDF report
        
        Args:
            output_path: percorso file PDF
            areas_data: lista di dict con dati aree
            total_lamps: numero totale lampade
        """
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        
        # Intestazione
        pdf.set_font('Helvetica', 'B', 18)
        pdf.cell(0, 10, self.t['title'], ln=True, align='C')
        
        pdf.set_font('Helvetica', size=10)
        pdf.cell(0, 8, f"{self.t['project']}: {self.project_name}", ln=True)
        pdf.cell(0, 8, f"{self.t['date']}: {self.timestamp.strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.ln(5)
        
        # Riepilogo aree
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, self.t['summary'], ln=True)
        pdf.set_font('Helvetica', size=9)
        
        # Tabella aree
        col_widths = [30, 25, 25, 25, 25, 35]
        headers = [
            self.t['area_name'],
            self.t['area_size'],
            self.t['lamps_required'],
            self.t['beam_width'],
            self.t['mounting_height'],
            self.t['photometry']
        ]
        
        # Intestazione tabella
        pdf.set_font('Helvetica', 'B', 9)
        for header, width in zip(headers, col_widths):
            pdf.cell(width, 7, header, border=1, align='C')
        pdf.ln()
        
        # Dati aree
        pdf.set_font('Helvetica', size=8)
        total_area = 0
        for area in areas_data:
            pdf.cell(col_widths[0], 6, area.get('name', 'N/A')[:20], border=1)
            area_size = area.get('surface', 0)
            total_area += area_size
            pdf.cell(col_widths[1], 6, f"{area_size:.1f}", border=1, align='R')
            pdf.cell(col_widths[2], 6, str(area.get('lamps', 0)), border=1, align='C')
            pdf.cell(col_widths[3], 6, f"{area.get('beam_width', 0):.2f}", border=1, align='R')
            pdf.cell(col_widths[4], 6, f"{area.get('height', 0):.2f}", border=1, align='R')
            photom = area.get('photometry_name', 'N/A')[:15]
            pdf.cell(col_widths[5], 6, photom, border=1)
            pdf.ln()
        
        # Totali
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(col_widths[0], 7, 'TOTALE', border=1)
        pdf.cell(col_widths[1], 7, f"{total_area:.1f}", border=1, align='R')
        pdf.cell(col_widths[2], 7, str(total_lamps), border=1, align='C')
        pdf.cell(sum(col_widths[3:]), 7, '', border=1)
        pdf.ln()
        
        pdf.ln(5)
        
        # Dettagli tecnici per area
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, self.t['areas'], ln=True)
        
        for idx, area in enumerate(areas_data):
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 7, f"{idx+1}. {area.get('name', f'Area_{idx+1}')}", ln=True)
            
            pdf.set_font('Helvetica', size=9)
            details = [
                (self.t['area_size'], f"{area.get('surface', 0):.2f} m²"),
                (self.t['lamps_required'], str(area.get('lamps', 0))),
                (self.t['beam_width'], f"{area.get('beam_width', 0):.2f} m"),
                (self.t['spacing_x'], f"{area.get('spacing_x', 0):.2f} m"),
                (self.t['spacing_y'], f"{area.get('spacing_y', 0):.2f} m"),
                (self.t['mounting_height'], f"{area.get('height', 0):.2f} m"),
                (self.t['uniformity'], f"{area.get('uniformity', 0):.1f}%"),
                (self.t['photometry'], area.get('photometry_name', 'N/A')),
            ]
            
            for label, value in details:
                pdf.cell(80, 5, f"{label}:", border=0)
                pdf.cell(0, 5, str(value), border=0, ln=True)
            
            pdf.ln(2)
        
        # Note tecniche
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 7, self.t['notes'], ln=True)
        pdf.set_font('Helvetica', size=8)
        note_text = (
            "- Calcoli semplificati per il design preliminare\n"
            "- Verificare sempre con misurazioni in situ\n"
            "- Considerare fattori di degrado e riflessioni ambientali\n"
            "- File generato da LUXiA v1.0"
        )
        pdf.multi_cell(0, 4, note_text)
        
        # Salva PDF
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pdf.output(output_path)
        return output_path
