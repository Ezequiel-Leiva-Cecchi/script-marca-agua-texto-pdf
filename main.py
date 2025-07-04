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


# -------------------------------------------------------------------------
# Función: crear_marca_agua
# Descripción: Genera un PDF en memoria con una marca de agua en diagonal
# que se repetirá sobre el documento original.
# -------------------------------------------------------------------------
def crear_marca_agua(texto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 18)  # Fuente y tamaño
    c.setFillColorRGB(0.09, 0.94, 0.92, alpha=0.50)  # Color con transparencia

    # Dibujamos el texto en diagonal en varias posiciones
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


# -------------------------------------------------------------------------
# Función: aplicar_marca
# Descripción: Superpone una marca de agua sobre cada página del PDF de entrada
# -------------------------------------------------------------------------
def aplicar_marca(pdf_entrada, pdf_salida, marca_pdf):
    lector = PdfReader(pdf_entrada)
    escritor = PdfWriter()

    # Para cada página del PDF, le agrega la marca de agua
    for pagina in lector.pages:
        pagina.merge_page(marca_pdf.pages[0])
        escritor.add_page(pagina)

    # Guarda el nuevo PDF en la ruta de salida
    with open(pdf_salida, "wb") as salida:
        escritor.write(salida)


# -------------------------------------------------------------------------
# Función: procesar_pdfs
# Descripción: Controla el flujo principal del script.
# Lee todos los PDFs de la carpeta de entrada, les aplica la marca,
# y guarda los resultados en la carpeta de salida.
# -------------------------------------------------------------------------
def procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca):
    # Verifica si existe la carpeta de entrada
    if not os.path.exists(carpeta_entrada):
        print(f"ERROR: La carpeta de entrada '{carpeta_entrada}' no existe.")
        return

    # Si la carpeta de salida no existe, la crea
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Crea el PDF con la marca de agua
    marca_pdf = crear_marca_agua(texto_marca)

    # Obtiene todos los archivos PDF de la carpeta de entrada
    archivos_pdf = [
        f for f in os.listdir(carpeta_entrada) if f.lower().endswith(".pdf")
    ]

    if not archivos_pdf:
        print("No se encontraron archivos PDF en la carpeta de entrada.")
        return

    # Procesa cada archivo PDF aplicando la marca de agua
    for archivo in archivos_pdf:
        ruta_entrada = os.path.join(carpeta_entrada, archivo)
        ruta_salida = os.path.join(carpeta_salida, archivo)
        aplicar_marca(ruta_entrada, ruta_salida, marca_pdf)
        print(f"Procesado el archivo: {archivo}")


# -------------------------------------------------------------------------
# Punto de entrada del script
# Define los nombres de las carpetas y el texto de la marca de agua
# Luego llama a la función principal para procesar los PDFs
# -------------------------------------------------------------------------
if __name__ == "__main__":
    carpeta_entrada = "documentos_originales"
    carpeta_salida = "documentos_marcados"
    texto_marca = "entiendayaprenda.com"

    procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca)
