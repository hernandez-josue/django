from xhtml2pdf import pisa

html = """
<html><head><style>
@page { size: a4; margin: 2cm; }
h1 { color: #0A2342; }
</style></head>
<body>
<h1>ERP Django - UTEC Celaya</h1>
<p>Prueba de PDF con xhtml2pdf</p>
</body></html>
"""

with open("prueba_xhtml2pdf.pdf", "wb") as f:
    resultado = pisa.CreatePDF(html, dest=f)

print("Errores:", resultado.err)
