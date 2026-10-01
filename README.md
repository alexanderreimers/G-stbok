# Gästbok

Inlämningsuppgift i Webbserverprogrammering (TE24). En gästbok byggd med Python och Flask.

## Funktioner

- Formulär med namn, ort (valfritt) och meddelande
- Varje inlägg får ett id och en tidpunkt
- Alla inlägg sparas i `data.json` (korrekt JSON-format)
- Inläggen skrivs ut via HTML-mallar (Jinja2) med mallarv: `base.html` → `index.html`, och `inlagg.html` för varje inlägg
- Kontroll av indata på servern, med felmeddelanden
- Nyaste inlägget visas först

## Struktur

```
app.py              Flask-appen (routes, läsa/spara JSON)
data.json           Alla inlägg
templates/          HTML-mallar
static/style.css    Stilmall
```

## Exempel på JSON

```json
[
    {
        "id": 1,
        "namn": "Alexander",
        "ort": "Täby",
        "meddelande": "Hej och välkommen till min gästbok!",
        "tid": "2026-10-01T15:04:00"
    }
]
```

## Kom igång

```
pip install flask
python app.py
```

Öppna sedan http://127.0.0.1:5000 i webbläsaren.
