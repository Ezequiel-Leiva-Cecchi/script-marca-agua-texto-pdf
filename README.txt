========================================
     Script de Marca de Agua en PDFs
========================================

Este programa permite aplicar automáticamente una marca de agua con el texto:
"entiendayaprenda.com"
a todos los archivos PDF ubicados dentro de la carpeta "documentos_originales".

Los archivos procesados se guardarán en la carpeta "documentos_marcados", manteniendo los archivos originales sin modificar.

----------------------------------------
▶️ ¿Cómo se usa?
----------------------------------------

1. Colocar todos los archivos PDF que quieran marcar dentro de la carpeta:
   documentos_originales
2. Ejecutar el archivo main.py con Python (haciendo doble clic o desde consola):
   - En Windows:
     Hacer doble clic en main.py
     o abrir PowerShell/CMD y ejecutar:
       python main.py

3. Al finalizar, los nuevos archivos con la marca estarán en:
   documentos_marcados

----------------------------------------
🔧 ¿Qué requisitos tiene?
----------------------------------------

- Tener Python instalado (recomendado Python 3.10 o superior)
- Tener las siguientes librerías:
  - pypdf
  - reportlab

Si hace falta instalarlas, usar este comando en la consola:

    pip install requirements.txt

----------------------------------------
ℹ️ Información adicional
----------------------------------------
- La marca de agua se aplica en diagonal con el texto repetido en la página.
- El diseño busca replicar el estilo original utilizado por Entienda y Aprenda.
- El script está preparado para funcionar de forma automática, sin intervención manual.
----------------------------------------
👨‍💻 Desarrollado por:
----------------------------------------
Ezequiel Leiva Cecchi
Versión 1.0 - Junio 2025