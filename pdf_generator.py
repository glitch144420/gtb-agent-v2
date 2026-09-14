import os
from typing import Optional
import re

class PDFGenerator:
    def __init__(self):
        pass
    
    def create_pdf(self, title: str, content: str, output_path: str) -> Optional[str]:
        """Create PDF - returns None if fails (non-critical)."""
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            
            # استخدام خط يدعم Unicode
            try:
                pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
                pdf.set_font("DejaVu", size=10)
            except:
                pdf.set_font("Arial", size=10)
            
            # العنوان
            pdf.set_font("DejaVu" if "DejaVu" in pdf.fonts else "Arial", 'B', 16)
            pdf.cell(0, 10, txt=title[:80], ln=True)
            pdf.ln(5)
            
            # المحتوى
            pdf.set_font("DejaVu" if "DejaVu" in pdf.fonts else "Arial", size=10)
            clean = re.sub(r'<[^>]+>', '', content)
            clean = clean.encode("latin-1", errors="ignore").decode("latin-1")
            
            for line in clean.split('\n')[:100]:
                line = line.strip()
                if line:
                    pdf.cell(0, 8, txt=line[:80], ln=True)
            
            pdf.output(output_path)
            return output_path
        except:
            return None
    
    def create_project_pdf(self, project_info, output_path):
        return self.create_pdf("Project", str(project_info), output_path)
