# Copyright (c) 2025 JOSE ROCHA. Todos los derechos reservados.
# modules/pdf_generator.py
# Generación del informe PDF

from fpdf import FPDF
from datetime import datetime

class ReportePDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "INFORME POSTVENTA", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

# -----------------------------------------------------------
# FUNCIÓN PRINCIPAL PARA CREAR EL PDF
# -----------------------------------------------------------

def generar_pdf(resumen: dict, ruta_salida="output/informe_postventa.pdf"):
    pdf = ReportePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # -------------------------------------------------------
    # 1. Portada
    # -------------------------------------------------------
    pdf.set_font("Arial", size=12)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.cell(0, 10, f"Fecha de generación: {fecha}", ln=True)
    pdf.ln(5)

    total_registros = resumen["conteo_por_area"][0][1]
    pdf.cell(0, 10, f"Total de registros procesados: {total_registros}", ln=True)
    pdf.ln(10)

    # -------------------------------------------------------
    # 2. MÉTRICAS
    # -------------------------------------------------------
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "RESUMEN GENERAL", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    # Total por estado
    pdf.cell(0, 8, "Total por estado:", ln=True)
    for estado, cantidad in resumen["total_por_estado"]:
        pdf.cell(0, 7, f"- {estado}: {cantidad}", ln=True)
    pdf.ln(5)

    # Top casas
    pdf.cell(0, 8, "Top 5 casas con más reportes:", ln=True)
    for casa, cantidad in resumen["top_5_casas"]:
        pdf.cell(0, 7, f"- {casa}: {cantidad}", ln=True)
    pdf.ln(5)

    # Top capítulos
    pdf.cell(0, 8, "Top 3 capítulos más frecuentes:", ln=True)
    for capitulo, cantidad in resumen["top_3_capitulos"]:
        pdf.cell(0, 7, f"- {capitulo}: {cantidad}", ln=True)
    pdf.ln(10)

    # -------------------------------------------------------
    # 3. GUARDAR
    # -------------------------------------------------------
    pdf.output(ruta_salida)
    print(f"✔ PDF generado correctamente: {ruta_salida}")
