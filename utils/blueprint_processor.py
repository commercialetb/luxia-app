import numpy as np
from PIL import Image
import io
import streamlit as st

try:
    import cv2
    HAS_CV2 = True
except Exception:
    # Catch broad exceptions (ImportError, OSError due to missing libGL, etc.)
    HAS_CV2 = False

class BlueprintProcessor:
    """Gestisce upload, visualizzazione e selezione aree su planimetrie"""
    
    def __init__(self, file_path=None, image=None):
        self.original_image = None
        self.display_image = None
        self.scale_factor = 1.0
        
        if file_path:
            self.load_from_file(file_path)
        elif image:
            # Converti PIL Image a numpy array
            if isinstance(image, Image.Image):
                self.original_image = np.array(image.convert('RGB'))
            else:
                self.original_image = image
            self.display_image = self.original_image.copy()
    
    def load_from_file(self, file_path):
        """Carica immagine da file (JPG, PNG)"""
        try:
            if HAS_CV2:
                img = cv2.imread(file_path)
                if img is None:
                    raise ValueError("Non riesco a leggere il file immagine")
                self.original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                # Fallback a PIL se cv2 non disponibile
                pil_img = Image.open(file_path).convert('RGB')
                self.original_image = np.array(pil_img)
            self.display_image = self.original_image.copy()
            return True
        except Exception as e:
            st.error(f"Errore nel caricamento: {str(e)}")
            return False
    
    def load_from_pil(self, pil_image):
        """Carica da PIL Image"""
        self.original_image = np.array(pil_image.convert('RGB'))
        self.display_image = self.original_image.copy()
    
    def resize_for_display(self, max_width=800, max_height=600):
        """Ridimensiona per il display mantenendo proporzioni"""
        h, w = self.original_image.shape[:2]
        scale = min(max_width/w, max_height/h, 1.0)
        
        if scale < 1.0:
            if HAS_CV2:
                new_w = int(w * scale)
                new_h = int(h * scale)
                self.display_image = cv2.resize(self.original_image, (new_w, new_h))
            else:
                # Fallback con PIL
                pil_img = Image.fromarray(self.original_image)
                new_w = int(w * scale)
                new_h = int(h * scale)
                pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                self.display_image = np.array(pil_img)
            self.scale_factor = scale
        else:
            self.display_image = self.original_image.copy()
            self.scale_factor = 1.0
    
    def get_pil_image(self):
        """Restituisce come PIL Image"""
        return Image.fromarray(self.display_image)
    
    def draw_areas(self, areas):
        """Disegna le aree selezionate"""
        img = self.display_image.copy()
        colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
        ]
        
        pil_img = Image.fromarray(img)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(pil_img)
        
        for idx, area in enumerate(areas):
            color = colors[idx % len(colors)]
            if area['type'] == 'rectangle':
                pts = area['points']
                if len(pts) >= 2:
                    pt1 = (int(pts[0][0]), int(pts[0][1]))
                    pt2 = (int(pts[1][0]), int(pts[1][1]))
                    draw.rectangle([pt1, pt2], outline=color, width=2)
            elif area['type'] == 'polygon':
                pts = [(int(p[0]), int(p[1])) for p in area['points']]
                if len(pts) >= 2:
                    draw.polygon(pts, outline=color)
            
            # Etichetta area
            if area['points']:
                x = int(area['points'][0][0])
                y = int(area['points'][0][1])
                draw.text((x, y-15), f"A{idx+1}", fill=color)
        
        return pil_img


def convert_dwg_to_image(dwg_file):
    """Converte DWG a immagine usando ezdxf"""
    try:
        import ezdxf
        doc = ezdxf.readfile(dwg_file)
        # Semplice rendering - per soluzioni robuste usare librerie specializzate
        st.warning("DWG support è semplificato. Usa JPG/PNG per migliori risultati.")
        return None
    except Exception as e:
        st.error(f"Errore conversione DWG: {str(e)}")
        return None


def convert_pdf_to_image(pdf_file):
    """Converte prima pagina PDF a immagine"""
    try:
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(pdf_file.read(), first_page=1, last_page=1)
        return images[0] if images else None
    except Exception as e:
        st.error(f"Errore conversione PDF: {str(e)}")
        return None
