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
# Función: crear_marca_texto_sin_link
# Descripción: Genera un PDF en memoria con una marca de agua en diagonal
# que se repetirá sobre el documento original SIN ningún enlace.
# -------------------------------------------------------------------------
def crear_marca_texto_sin_link(texto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(0.09, 0.94, 0.92, alpha=0.50)

    # Dibujar muchas marcas 
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
# Función: crear_link_individual
# Descripción: Genera un PDF con un pequeño texto con hipervínculo
# ubicado abajo a la derecha. Solo este texto será clickeable.
# -------------------------------------------------------------------------
def crear_link_individual(texto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.09, 0.94, 0.92, alpha=0.50)

    x_link = 450
    y_link = 50
    ancho_link = c.stringWidth(texto, "Helvetica", 12)
    alto_link = 12

    c.drawString(x_link, y_link, texto)

    c.linkURL(
        "https://entiendayaprenda.com",
        rect=(x_link, y_link, x_link + ancho_link, y_link + alto_link),
        relative=0,
        thickness=0,
    )

    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


# -------------------------------------------------------------------------
# Función: aplicar_marca
# Descripción: Superpone dos capas sobre cada página del PDF de entrada:
# - una con marcas de agua en diagonal sin links
# - otra con un único texto clickeable en la esquina
# -------------------------------------------------------------------------
def aplicar_marca(pdf_entrada, pdf_salida, marca_texto, marca_link):
    lector = PdfReader(pdf_entrada)
    escritor = PdfWriter()

    for pagina in lector.pages:
        pagina.merge_page(marca_texto.pages[0])
        pagina.merge_page(marca_link.pages[0])
        escritor.add_page(pagina)

    with open(pdf_salida, "wb") as salida:
        escritor.write(salida)


# -------------------------------------------------------------------------
# Función: procesar_pdfs
# Descripción: Controla el flujo principal del script.
# Lee los archivos PDF de una carpeta de entrada y sus subcarpetas, 
# les aplica la marca de agua y los guarda en una carpeta de salida
# manteniendo la estructura de directorios.
# -------------------------------------------------------------------------
def procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca):
    if not os.path.exists(carpeta_entrada):
        print(f"ERROR: La carpeta de entrada '{carpeta_entrada}' no existe.")
        return

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    marca_texto = crear_marca_texto_sin_link(texto_marca)
    marca_link = crear_link_individual(texto_marca)

    # Contador para archivos procesados
    archivos_procesados = 0

    # Recorrer recursivamente todas las carpetas y subcarpetas
    for ruta_actual, subcarpetas, archivos in os.walk(carpeta_entrada):
        # Calcular la ruta relativa desde la carpeta de entrada
        ruta_relativa = os.path.relpath(ruta_actual, carpeta_entrada)
        
        # Crear la carpeta correspondiente en la salida
        carpeta_salida_actual = os.path.join(carpeta_salida, ruta_relativa)
        if not os.path.exists(carpeta_salida_actual):
            os.makedirs(carpeta_salida_actual)

        # Procesar archivos PDF en la carpeta actual
        archivos_pdf = [f for f in archivos if f.lower().endswith(".pdf")]
        
        for archivo in archivos_pdf:
            ruta_entrada = os.path.join(ruta_actual, archivo)
            ruta_salida = os.path.join(carpeta_salida_actual, archivo)
            
            try:
                aplicar_marca(ruta_entrada, ruta_salida, marca_texto, marca_link)
                archivos_procesados += 1
                print(f"Procesado: {os.path.join(ruta_relativa, archivo)}")
            except Exception as e:
                print(f"Error procesando {archivo}: {str(e)}")

    if archivos_procesados == 0:
        print("No se encontraron archivos PDF en la carpeta de entrada ni en sus subcarpetas.")
    else:
        print(f"\nProcesamiento completado. Se procesaron {archivos_procesados} archivos PDF.")


# -------------------------------------------------------------------------
# Punto de entrada del script
# -------------------------------------------------------------------------
if __name__ == "__main__":
    carpeta_entrada = "documentos_originales"
    carpeta_salida = "documentos_marcados"
    texto_marca = "entiendayaprenda.com"

    procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca)
