from fpdf import FPDF
import sys
import os

class SafePremiumPDF(FPDF):
    def header(self):
        # Fondo oscuro para el encabezamiento
        self.set_fill_color(0, 43, 91)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Courier', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'INDUSTRIAL SCL DOCUMENTATION', 0, 1, 'C')
        self.set_font('Courier', 'I', 10)
        self.cell(0, 5, 'Standard IEC 61131-3 | Siemens SIMATIC', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-20)
        self.set_font('Courier', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def md_to_pdf(input_path, output_path):
    pdf = SafePremiumPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        text = line.strip()
        if not text:
            pdf.ln(5)
            continue
            
        # Eliminar caracteres raros para evitar errores en Python 3.14 / FPDF2
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        
        if safe_text.startswith('# '):
            pdf.set_font('Courier', 'B', 16)
            pdf.set_text_color(0, 43, 91)
            pdf.multi_cell(0, 10, safe_text[2:])
            pdf.ln(2)
        elif safe_text.startswith('## '):
            pdf.set_font('Courier', 'B', 14)
            pdf.set_text_color(0, 80, 150)
            pdf.multi_cell(0, 10, safe_text[3:])
        elif safe_text.startswith('- '):
            pdf.set_font('Courier', '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, f'  * {safe_text[2:]}')
        else:
            pdf.set_font('Courier', '', 11)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 7, safe_text)

    pdf.output(output_path)
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        md_to_pdf(sys.argv[1], sys.argv[2])
