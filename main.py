# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Script en Python para agregar marcas de agua a PDFs.
# Lee todos los archivos PDF de una carpeta de entrada,
# les aplica una marca de agua personalizada y los guarda en otra carpeta.
# Autor: Ezequiel
# -------------------------------------------------------------------------

import os
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def crear_marca_agua(texto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(0.09, 0.94, 0.92, alpha=0.50)  # Color con transparencia

    # Dibujamos el texto repetido en diagonal en distintas posiciones
    for y in range(-200, 1000, 400):
        for x in range(-200, 800, 130):
            c.saveState()
            c.translate(x, y)
            c.rotate(45)
            c.drawString(0, 0, texto)
            c.restoreState()

    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


def aplicar_marca(pdf_entrada, pdf_salida, marca_pdf):
    lector = PdfReader(pdf_entrada)
    escritor = PdfWriter()

    for pagina in lector.pages:
        pagina.merge_page(marca_pdf.pages[0])
        escritor.add_page(pagina)

    with open(pdf_salida, "wb") as salida:
        escritor.write(salida)


def procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca):
    if not os.path.exists(carpeta_entrada):
        print(f"ERROR: La carpeta de entrada '{carpeta_entrada}' no existe.")
        return

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    marca_pdf = crear_marca_agua(texto_marca)

    archivos_pdf = [
        f for f in os.listdir(carpeta_entrada) if f.lower().endswith(".pdf")
    ]

    if not archivos_pdf:
        print("No se encontraron archivos PDF en la carpeta de entrada.")
        return

    for archivo in archivos_pdf:
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        ruta_salida = os.path.join(carpeta_salida, archivo)
        aplicar_marca(ruta_entrada, ruta_salida, marca_pdf)
        print(f"Procesado el archivo: {archivo}")


if __name__ == "__main__":
    carpeta_entrada = "documentos_originales"
    carpeta_salida = "documentos_marcados"
    texto_marca = "texto de la marca de agua"

    if texto_marca.strip() == "texto de la marca de agua":
        print(
            "ATENCIÓN: Estás usando el texto de marca de agua por defecto. Modificalo si es necesario.\n"
        )

    procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca)