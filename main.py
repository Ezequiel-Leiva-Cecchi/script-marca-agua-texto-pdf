# -------------------------------------------------------------------------
# Script en Python para agregar marcas de agua a PDFs.
# Lee todos los archivos PDF de una carpeta de entrada,
# les aplica una marca de agua personalizada y los guarda en otra carpeta.
# Autor: Ezequiel (modificado: tamaño/opacidad de marca)
# -------------------------------------------------------------------------

import os
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color  # uso Color(...) para controlar alpha

# -------------------------------------------------------------------------
# Función: crear_marca_texto
# Descripción: Genera un PDF en memoria con una marca de agua en diagonal,
# centrada y grande, que se adapta al tamaño de cada página.
# El texto principal es un hipervínculo clickeable (ajustado por letra).
# -------------------------------------------------------------------------
def crear_marca_texto(texto_principal, texto_secundario, ancho, alto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(ancho, alto))
    c.saveState()

    # 🔹 Trasladar y rotar al centro de la página
    c.translate(ancho / 2, alto / 2)
    c.rotate(45)

    # ---------------------------
    # Texto principal (link)
    # ---------------------------
    font_size_link = 80  # <<-- Aumentado (más grande)
    c.setFont("Helvetica-Bold", font_size_link)
    # <<-- Más opaco: color azul con alpha alto
    c.setFillColor(Color(0.0, 0.7, 1.0, alpha=0.40))

    texto_y = 30
    c.drawCentredString(0, texto_y, texto_principal)

    # Calcular ancho total del texto
    ancho_texto = c.stringWidth(texto_principal, "Helvetica-Bold", font_size_link)

    # 🔹 Crear links por cada letra (más ajustado al texto real)
    x_cursor = -ancho_texto / 2
    for letra in texto_principal:
        ancho_letra = c.stringWidth(letra, "Helvetica-Bold", font_size_link)
        rect = (
            x_cursor,
            texto_y - font_size_link * 0.18,
            x_cursor + ancho_letra,
            texto_y + font_size_link * 0.72,
        )
        c.linkURL(
            "https://entiendayaprenda.com",
            rect=rect,
            relative=1,  # relativo al sistema de coordenadas rotado
            thickness=0,
        )
        x_cursor += ancho_letra

    # ---------------------------
    # Texto secundario (mensaje)
    # ---------------------------
    font_size_msg = 47  # ligeramente más grande también
    c.setFont("Helvetica", font_size_msg)
    # más opaco para el secundario
    c.setFillColor(Color(0.0, 0.5, 1.0, alpha=0.50))
    c.drawCentredString(0, -60, texto_secundario)

    c.restoreState()
    c.save()
    buffer.seek(0)
    return PdfReader(buffer)


# -------------------------------------------------------------------------
# Función: aplicar_marca
# Descripción: Superpone sobre cada página del PDF de entrada:
# - una marca de agua diagonal central con link
# -------------------------------------------------------------------------
def aplicar_marca(pdf_entrada, pdf_salida, texto_marca):
    lector = PdfReader(pdf_entrada)
    escritor = PdfWriter()
    mensaje = "¡Aprendé con los mejores profes particulares!"
    for pagina in lector.pages:
        ancho = float(pagina.mediabox.width)
        alto = float(pagina.mediabox.height)
        # Marca de agua diagonal central con link
        marca_texto = crear_marca_texto(texto_marca, mensaje, ancho, alto)
        pagina.merge_page(marca_texto.pages[0])
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

    archivos_procesados = 0

    # Recorrer recursivamente todas las carpetas y subcarpetas
    for ruta_actual, subcarpetas, archivos in os.walk(carpeta_entrada):
        ruta_relativa = os.path.relpath(ruta_actual, carpeta_entrada)
        carpeta_salida_actual = os.path.join(carpeta_salida, ruta_relativa)
        if not os.path.exists(carpeta_salida_actual):
            os.makedirs(carpeta_salida_actual)

        archivos_pdf = [f for f in archivos if f.lower().endswith(".pdf")]
        
        for archivo in archivos_pdf:
            ruta_entrada = os.path.join(ruta_actual, archivo)
            ruta_salida = os.path.join(carpeta_salida_actual, archivo)
            
            try:
                aplicar_marca(ruta_entrada, ruta_salida, texto_marca)
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
