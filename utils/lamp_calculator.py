import math
import numpy as np
import ezdxf
from ezdxf.entities import LWPolyline
from datetime import datetime

class LampPlacementCalculator:
    """Calcola numero lampade, passo e posizionamento in base alle aree"""
    
    def __init__(self, photometry_data=None):
        self.photometry = photometry_data or {}
    
    def calculate_spacing(self, area_width, area_height, beam_width):
        """
        Calcola il passo ottimale (spacing) tra lampade
        
        Args:
            area_width: larghezza area in m
            area_height: altezza area in m
            beam_width: larghezza fascio luminoso in m
        
        Returns:
            dict con numero lampade, spacing x, spacing y
        """
        # Utilizziamo il 70% della larghezza del fascio per avere sovrapposizione
        spacing = beam_width * 0.7
        
        if spacing <= 0:
            spacing = 1.0
        
        # Calcola numero di lampade lungo X e Y
        n_x = max(1, math.ceil(area_width / spacing))
        n_y = max(1, math.ceil(area_height / spacing))
        total_lamps = n_x * n_y
        
        # Calcola spacing reale per riempire bene l'area
        actual_spacing_x = area_width / n_x if n_x > 0 else area_width
        actual_spacing_y = area_height / n_y if n_y > 0 else area_height
        
        return {
            'total_lamps': total_lamps,
            'lamps_x': n_x,
            'lamps_y': n_y,
            'spacing_x': actual_spacing_x,
            'spacing_y': actual_spacing_y,
            'coverage_width': n_x * spacing,
            'coverage_height': n_y * spacing,
        }
    
    def generate_lamp_positions(self, area_polygon, beam_width, start_offset=0.5):
        """
        Genera posizioni delle lampade all'interno di un poligono area
        
        Args:
            area_polygon: lista di punti [(x,y), (x,y), ...] che definiscono l'area
            beam_width: larghezza del fascio luminoso
            start_offset: offset di partenza dal bordo (m)
        
        Returns:
            lista di [(x, y), ...] con coordinate lampade
        """
        if not area_polygon or len(area_polygon) < 2:
            return []
        
        # Calcola bounding box dell'area
        xs = [p[0] for p in area_polygon]
        ys = [p[1] for p in area_polygon]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = max_x - min_x
        height = max_y - min_y
        
        # Calcola spacing
        spacing_config = self.calculate_spacing(width, height, beam_width)
        spacing_x = spacing_config['spacing_x']
        spacing_y = spacing_config['spacing_y']
        
        # Genera griglia di posizioni
        positions = []
        x = min_x + start_offset
        while x < max_x:
            y = min_y + start_offset
            while y < max_y:
                # Controlla se il punto è dentro il poligono
                if self._point_in_polygon((x, y), area_polygon):
                    positions.append((x, y))
                y += spacing_y
            x += spacing_x
        
        return positions
    
    @staticmethod
    def _point_in_polygon(point, polygon):
        """Ray casting algorithm per verificare se punto è dentro poligono"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def export_to_dwg(self, filepath, areas_data, scale=1.0):
        """
        Esporta layout con aree e lampade a DWG
        
        Args:
            filepath: percorso file DWG di output
            areas_data: lista di dict con aree e dati lampade
            scale: fattore di scala per il disegno
        """
        # Crea nuovo DWG
        dwg = ezdxf.new('R2010')
        msp = dwg.modelspace()
        
        # Aggiunge layer per diversi elementi
        dwg.layers.new(name='Areas', dxfattribs={'color': 5})
        dwg.layers.new(name='Lamps', dxfattribs={'color': 1})
        dwg.layers.new(name='Grid', dxfattribs={'color': 8})
        
        for area_idx, area_data in enumerate(areas_data):
            area_name = area_data.get('name', f'Area_{area_idx+1}')
            points = area_data.get('points', [])
            lamp_positions = area_data.get('lamp_positions', [])
            
            # Disegna area come poligono chiuso
            if len(points) >= 2:
                scaled_points = [(p[0]*scale, p[1]*scale) for p in points]
                
                # Chiudi il poligono
                if scaled_points[0] != scaled_points[-1]:
                    scaled_points.append(scaled_points[0])
                
                polyline = msp.add_lwpolyline(scaled_points, dxfattribs={
                    'layer': 'Areas',
                    'color': 5
                })
                
                # Aggiungi label area
                if scaled_points:
                    x, y = scaled_points[0]
                    msp.add_text(area_name, dxfattribs={
                        'height': 0.5,
                        'layer': 'Areas'
                    }).set_pos((x, y, 0))
            
            # Disegna lampade come cerchi
            lamp_radius = 0.1 * scale  # Rappresenta lampada come cerchio 0.2m dia
            for lamp_pos in lamp_positions:
                x, y = lamp_pos
                scaled_x, scaled_y = x * scale, y * scale
                
                # Aggiungi cerchio per rappresentare lampada
                msp.add_circle((scaled_x, scaled_y), lamp_radius, dxfattribs={
                    'layer': 'Lamps',
                    'color': 1
                })
                
                # Aggiungi punto di riferimento
                msp.add_point((scaled_x, scaled_y), dxfattribs={
                    'layer': 'Lamps',
                    'color': 1
                })
        
        # Salva file
        dwg.saveas(filepath)
        return filepath


def estimate_footcandles_per_lamp(lumen_output, area_coverage):
    """Stima illuminamento medio semplice"""
    if area_coverage <= 0:
        return 0
    # Semplice lumen/area (ignora molti fattori reali)
    return lumen_output / area_coverage
