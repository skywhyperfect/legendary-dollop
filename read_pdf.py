import sys

try:
    import PyPDF2
    reader = PyPDF2.PdfReader('FINAL.pdf')
    for page in reader.pages:
        print(page.extract_text())
except Exception as e:
    import os
    os.system('pdftotext FINAL.pdf -')
