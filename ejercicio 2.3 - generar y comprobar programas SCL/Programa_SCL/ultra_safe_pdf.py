from fpdf import FPDF
import sys

class UltraSafePDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'DOCUMENTACION SCL', 0, 1, 'C')

def create_pdf(in_md, out_pdf):
    pdf = UltraSafePDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=11)
    
    with open(in_md, 'r', encoding='utf-8') as f:
        for line in f:
            # Just write the text without fancy layout
            clean = line.encode('ascii', 'ignore').decode('ascii')
            pdf.write(7, clean)
            
    pdf.output(out_pdf)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        create_pdf(sys.argv[1], sys.argv[2])
