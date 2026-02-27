from fpdf import FPDF
import sys

def create_simple_pdf(text, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, txt=text, ln=1, align="C")
    pdf.output(output_pdf)

if __name__ == "__main__":
    create_simple_pdf("Hola Mundo SCL", "test_simple.pdf")
