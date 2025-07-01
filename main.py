import os
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Crear una maca de agua repetida en diagonal por toda la hoja
def crear_marca_agua(texto):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 18)  # Fuente y tamaño del texto
    c.setFillColorRGB(0.09, 0.94, 0.92, alpha=0.50)  # Color del texto

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


# Agregar la marca de agua a un PDF existente
def aplicar_marca(pdf_entrada, pdf_salida, marca_pdf):
    lector = PdfReader(pdf_entrada)
    escritor = PdfWriter()

    for pagina in lector.pages:
        pagina.merge_page(marca_pdf.pages[0])
        escritor.add_page(pagina)
    with open(pdf_salida, "wb") as salida:
        escritor.write(salida)


# Procesa todos los archivos Pdf de la carpeta de entrada
def procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    marca_pdf = crear_marca_agua(texto_marca)

    for archivo in os.listdir(carpeta_entrada):
        if archivo.lower().endswith(".pdf"):
            ruta_entrada = os.path.join(carpeta_entrada, archivo)
            ruta_salida = os.path.join(carpeta_salida, archivo)
            aplicar_marca(ruta_entrada, ruta_salida, marca_pdf)
            print(f"Procesado el archivo: {archivo}")


# Punto de entrada del script
if __name__ == "__main__":
    carpeta_entrada = "documentos_originales"
    carpeta_salida = "documentos_marcados"
    texto_marca = "texto de la marca de agua"
    procesar_pdfs(carpeta_entrada, carpeta_salida, texto_marca)
