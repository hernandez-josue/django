import re, shutil
from pathlib import Path

BASE = Path("templates/base.html")
BIEN = Path("templates/bienvenida.html")
ADMIN = Path("templates/admin/base_site.html")

html = BASE.read_text(encoding="utf-8")
shutil.copy(BASE, "templates/base.html.bak")   # respaldo por si acaso

# 1) Limpiar lo que se duplicó en intentos anteriores
html = re.sub(r"[ \t]*\{%\s*block extra_js\s*%\}\s*\{%\s*endblock\s*%\}[ \t]*\n?", "", html)
html = re.sub(r"[ \t]*\{%\s*include \"_spotify_player\.html\"\s*%\}[ \t]*\n?", "", html)
html = re.sub(r"[ \t]*<!-- Reproductor de música flotante -->[ \t]*\n?", "", html)
html = re.sub(r"[ \t]*<!-- Turbo:.*?</script>[ \t]*\n?", "", html, flags=re.S)
html = re.sub(r"[ \t]*<meta name=\"turbo-cache-control\"[^>]*>[ \t]*\n?", "", html)

# 2) Turbo en el <head>, antes de extra_css
turbo = '''    <!-- Turbo: navega sin recargar para que la música no se corte -->
    <meta name="turbo-cache-control" content="no-cache">
    <script type="module">
        import { setFormMode } from "https://cdn.jsdelivr.net/npm/@hotwired/turbo@8.0.4/dist/turbo.es2017-esm.min.js";
        setFormMode("off");
    </script>
    '''
html = html.replace("{% block extra_css %}{% endblock %}",
                    turbo + "{% block extra_css %}{% endblock %}", 1)

# 3) Link del Admin sin Turbo (Jazzmin)
html = re.sub(r'<a href="/admin/" class="erp-nav-link"(?![^>]*data-turbo)',
              '<a href="/admin/" class="erp-nav-link" data-turbo="false"', html)

# 4) Mover Tienda + carrito adentro del navbar (antes del link Admin)
m = re.search(
    r"<!-- En templates/base\.html.*?-->\s*"
    r"(<a href=\"\{% url 'catalogo:catalogo' %\}\".*?</a>)\s*"
    r"<!-- Contador.*?-->\s*"
    r"(\{% if carrito_total_items > 0 %\}.*?\{% endif %\})", html, flags=re.S)
if m:
    bloque = "        " + m.group(1) + "\n\n        " + m.group(2) + "\n\n        "
    html = html.replace(m.group(0), "")
    html = html.replace('<a href="/admin/"', bloque + '<a href="/admin/"', 1)

# 5) Reproductor + UN solo extra_js al final
html = html.replace("</body>",
    '<!-- Reproductor de música flotante -->\n{% include "_spotify_player.html" %}\n\n'
    '{% block extra_js %}{% endblock %}\n</body>', 1)

BASE.write_text(html, encoding="utf-8")
print("✔ base.html actualizado (respaldo: base.html.bak)")

# 6) bienvenida.html: tarjetas con Turbo
if BIEN.exists():
    b = BIEN.read_text(encoding="utf-8")
    b = b.replace("window.location='{{ m.url }}'", "Turbo.visit('{{ m.url }}')")
    BIEN.write_text(b, encoding="utf-8")
    print("✔ bienvenida.html actualizado")

# 7) Admin (Jazzmin): incluir el reproductor
ADMIN.parent.mkdir(parents=True, exist_ok=True)
if not ADMIN.exists():
    ADMIN.write_text('''{% extends "admin/base.html" %}
{% block extrajs %}
{{ block.super }}
{% include "_spotify_player.html" %}
{% endblock %}
''', encoding="utf-8")
    print("✔ admin/base_site.html creado")