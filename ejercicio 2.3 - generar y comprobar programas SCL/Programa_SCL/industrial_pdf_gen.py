from fpdf import FPDF
import sys
import os

class IndustrialPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 50, 100)
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'INDUSTRIAL SCL DOCUMENTATION', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate(in_md, out_pdf):
    pdf = IndustrialPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=11)
    pdf.set_text_color(0, 0, 0)
    
    with open(in_md, 'r', encoding='utf-8') as f:
        for line in f:
            t = line.strip()
            # Clean non-ASCII for safety on 3.14
            safe = t.encode('ascii', 'ignore').decode('ascii')
            
            if safe.startswith('# '):
                pdf.ln(5)
                pdf.set_font('helvetica', 'B', 14)
                pdf.cell(0, 10, safe[2:], ln=1)
                pdf.set_font('helvetica', size=11)
            elif safe.startswith('## '):
                pdf.ln(3)
                pdf.set_font('helvetica', 'B', 12)
                pdf.cell(0, 8, safe[3:], ln=1)
                pdf.set_font('helvetica', size=11)
            elif not safe:
                pdf.ln(5)
            else:
                # Use write for automated wrapping which we found stays safe
                pdf.write(7, safe + "\n")
                
    pdf.output(out_pdf)
    print(f"Generated {out_pdf}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        generate(sys.argv[1], sys.argv[2])
