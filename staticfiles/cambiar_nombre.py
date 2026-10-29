from pathlib import Path

CAMBIOS = [
    (" · UTEC Celaya · Espiral 1 W02", ""),
    ("Inicio · UTEC Celaya", "Inicio · Chinos S.A. de C.V."),
    ("ERP UTEC Celaya", "Chinos S.A. de C.V."),
    ("UTEC Celaya", "Chinos S.A. de C.V."),
    ("ERP Django", "Chinos S.A. de C.V."),
    ("Panel de administración Django", "Panel de administración"),
    ("Django 4.2 LTS", "Inventario"),
    ("Python 3.11", "Ventas"),
    ("Fable 5 AzulERP", "Reportes"),
]
SALTAR = {"env_erp", "staticfiles", ".git", "node_modules"}

for p in Path(".").rglob("*.html"):
    if SALTAR & set(p.parts) or "templates" not in p.parts:
        continue
    try:
        txt = p.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        print("SALTADO (codificacion):", p)
        continue
    nuevo = txt
    for viejo, reemplazo in CAMBIOS:
        nuevo = nuevo.replace(viejo, reemplazo)
    if nuevo != txt:
        p.write_bytes(nuevo.encode("utf-8"))
        print("Actualizado:", p)