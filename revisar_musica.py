from pathlib import Path

for f in Path("templates").rglob("*.html"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    n_inc = t.count("_spotify_player.html")
    n_div = t.count('id="spotify-player"')
    n_old = sum(t.count(x) for x in ("spotify-toggle", "sp-bubble", "open.spotify.com/embed/track"))
    if n_inc or n_div or n_old:
        print(f"{f}: include={n_inc} | div_player={n_div} | restos_viejos={n_old}")