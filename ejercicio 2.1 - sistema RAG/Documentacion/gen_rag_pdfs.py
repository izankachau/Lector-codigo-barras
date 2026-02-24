import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

def get_font():
    try:
        font_path = "C:/Windows/Fonts/arial.ttf"
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        return 'Arial'
    except:
        return 'Helvetica'

def create_premium_pdf(input_md, output_pdf, main_title, subtitle):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    font_name = get_font()
    primary_color = colors.HexColor("#1A1A1A")
    accent_color = colors.HexColor("#007AFF") 
    secondary_color = colors.HexColor("#555555")

    style_label = ParagraphStyle('Label', fontName=font_name, fontSize=8, textColor=accent_color, fontStyle='Bold', textTransform='uppercase', letterSpacing=2, spaceAfter=0.1*cm)
    style_title = ParagraphStyle('Title', fontName=font_name, fontSize=24, leading=28, textColor=primary_color, fontStyle='Bold', spaceAfter=0.2*cm)
    style_h1 = ParagraphStyle('H1', fontName=font_name, fontSize=14, leading=18, textColor=primary_color, fontStyle='Bold', textTransform='uppercase', spaceBefore=0.7*cm, spaceAfter=0.3*cm)
    style_h2 = ParagraphStyle('H2', fontName=font_name, fontSize=11, leading=14, textColor=accent_color, fontStyle='Bold', spaceBefore=0.4*cm, spaceAfter=0.2*cm)
    style_content = ParagraphStyle('Content', fontName=font_name, fontSize=10, leading=14, textColor=primary_color, alignment=TA_JUSTIFY, spaceAfter=0.3*cm)
    style_list = ParagraphStyle('List', parent=style_content, leftIndent=0.8*cm, firstLineIndent=-0.4*cm, spaceAfter=0.2*cm)

    elements = []
    elements.append(Paragraph(subtitle, style_label))
    elements.append(Paragraph(main_title, style_title))
    elements.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=0.8*cm))

    with open(input_md, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line: continue
        processed = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        if line.startswith('# '): continue 
        elif line.startswith('## '):
            elements.append(Paragraph(processed.replace('## ', ''), style_h1))
            elements.append(HRFlowable(width="20%", thickness=2, color=accent_color, hAlign='LEFT', spaceAfter=0.2*cm))
        elif line.startswith('### '):
            elements.append(Paragraph(processed.replace('### ', ''), style_h2))
        elif line.startswith('- ') or line.startswith('* '):
            elements.append(Paragraph(f"<font color='#007AFF'>●</font>  {processed.lstrip('-* ')}", style_list))
        else:
            elements.append(Paragraph(processed, style_content))

    elements.append(Spacer(1, 2*cm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=secondary_color))
    footer_data = [[Paragraph("<font size='8' color='#666666'>EXAMEN INFORMÁTICA 2026</font>", style_content),
                    Paragraph("<font size='8' color='#666666'>PROYECTO 2.1: SISTEMA RAG</font>", style_content),
                    Paragraph("<font size='8' color='#666666'>PÁGINA 1</font>", style_content)]]
    footer_table = Table(footer_data, colWidths=[6*cm, 6*cm, 6*cm])
    footer_table.setStyle(TableStyle([('ALIGN', (0,0), (0,0), 'LEFT'), ('ALIGN', (1,0), (1,0), 'CENTER'), ('ALIGN', (2,0), (2,0), 'RIGHT')]))
    elements.append(footer_table)

    doc.build(elements)

if __name__ == "__main__":
    base_path = r"c:\Users\izan1\Desktop\Lector código de barras\Examen_Informatica\ejercicio 2.1 - sistema RAG\Documentacion"
    
    # Listado de archivos a generar
    files_to_gen = [
        ("Investigacion_RAG.md", "01_Investigacion_Estado_Arte_RAG.pdf", "ESTADO DEL ARTE RAG 2024-2025", "INFORME TÉCNICO DE INVESTIGACIÓN"),
        ("Guia_Implementacion_RAG.md", "02_Guia_Implementacion_Paso_a_Paso.pdf", "GUÍA DE IMPLEMENTACIÓN RAG", "MANUAL TÉCNICO DE PROCEDIMIENTO"),
        ("Instrucciones_Uso_RAG.md", "03_Instrucciones_de_Uso_Aplicacion.pdf", "INSTRUCCIONES DE USO RAG", "MANUAL DE USUARIO FINAL")
    ]
    
    for md, pdf, title, sub in files_to_gen:
        create_premium_pdf(os.path.join(base_path, md), os.path.join(base_path, pdf), title, sub)
    
    print("PDFs generados con éxito.")
