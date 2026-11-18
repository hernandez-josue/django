import re, shutil
from pathlib import Path

T = Path("templates")
PLAYER = T / "_spotify_player.html"
INC = re.compile(r"[ \t]*\{%\s*include\s+[\"']_spotify_player\.html[\"']\s*%\}[ \t]*\n?")

def backup(f):
    b = f.with_suffix(f.suffix + ".bak2")
    if not b.exists():
        shutil.copy(f, b)

# 1) Quitar reproductores viejos pegados en otras plantillas
for f in T.rglob("*.html"):
    if f == PLAYER:
        continue
    t = f.read_text(encoding="utf-8", errors="ignore")
    o = t

    # bloque viejo inline: desde su comentario/div hasta el último </script> que le sigue
    m = re.search(r'(<!--\s*Reproductor[^>]*-->\s*)?<div id="spotify-player"', t)
    if m:
        fin = t.find("</script>", m.start())
        while fin != -1:
            sig = t.find("</script>", fin + 9)
            if sig == -1 or "<div" in t[fin:sig] and "toggleSpotify" not in t[fin:sig]:
                break
            fin = sig
        if fin != -1:
            t = t[:m.start()] + t[fin + 9:]

    # includes repetidos: solo se permite uno
    incs = list(INC.finditer(t))
    for x in reversed(incs[1:]):
        t = t[:x.start()] + t[x.end():]

    if t != o:
        backup(f)
        f.write_text(t, encoding="utf-8")
        print("✔ limpiado:", f)

# 2) _spotify_player.html: dejar una sola copia completa
p = PLAYER.read_text(encoding="utf-8")
starts = [m.start() for m in re.finditer(r'<div id="spotify-player"', p)]
if len(starts) > 1:
    backup(PLAYER)
    fin = p.find("</script>\n</div>", starts[0])
    fin = fin + len("</script>\n</div>") if fin != -1 else starts[1]
    PLAYER.write_text(p[:fin].rstrip() + "\n", encoding="utf-8")
    print("✔ _spotify_player.html tenía", len(starts), "copias → dejé 1")
else:
    print("• _spotify_player.html: 1 sola copia")

# 3) Resumen final
print("\n--- RESUMEN ---")
for f in T.rglob("*.html"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    i = len(INC.findall(t)); d = t.count('id="spotify-player"')
    if i or d:
        print(f"{f}: include={i} div_player={d}")