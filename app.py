# Gästbok – steg 3 (A-nivå)
# Alla inlägg sparas i korrekt JSON-format (data.json)
# och skrivs ut via HTML-mallar (Jinja2 med mallarv).
import json
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATAFIL = os.path.join(os.path.dirname(__file__), "data.json")

MAX_NAMN = 60
MAX_ORT = 60
MAX_MEDDELANDE = 500


def las_inlagg():
    """Läser alla inlägg från JSON-filen. Returnerar en tom lista om filen saknas."""
    try:
        with open(DATAFIL, "r", encoding="utf-8") as fil:
            return json.load(fil)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def spara_inlagg(lista):
    """Skriver hela listan med inlägg till JSON-filen."""
    with open(DATAFIL, "w", encoding="utf-8") as fil:
        json.dump(lista, fil, ensure_ascii=False, indent=4)


def kontrollera(namn, ort, meddelande):
    """Returnerar en lista med felmeddelanden (tom lista = allt ok)."""
    fel = []
    if not namn:
        fel.append("Du måste skriva ditt namn.")
    elif len(namn) > MAX_NAMN:
        fel.append(f"Namnet får vara högst {MAX_NAMN} tecken.")
    if len(ort) > MAX_ORT:
        fel.append(f"Orten får vara högst {MAX_ORT} tecken.")
    if not meddelande:
        fel.append("Du måste skriva ett meddelande.")
    elif len(meddelande) > MAX_MEDDELANDE:
        fel.append(f"Meddelandet får vara högst {MAX_MEDDELANDE} tecken.")
    return fel


@app.route("/", methods=["GET", "POST"])
def index():
    fel = []
    formular = {"namn": "", "ort": "", "meddelande": ""}

    if request.method == "POST":
        formular = {
            "namn": request.form.get("namn", "").strip(),
            "ort": request.form.get("ort", "").strip(),
            "meddelande": request.form.get("meddelande", "").strip(),
        }
        fel = kontrollera(**formular)

        if not fel:
            lista = las_inlagg()
            nytt_id = max((post["id"] for post in lista), default=0) + 1
            lista.append({
                "id": nytt_id,
                "namn": formular["namn"],
                "ort": formular["ort"],
                "meddelande": formular["meddelande"],
                "tid": datetime.now().isoformat(timespec="seconds"),
            })
            spara_inlagg(lista)
            # Omdirigera så att inlägget inte skickas igen om sidan laddas om
            return redirect(url_for("index", tack=1))

    # Nyaste inlägget först
    inlagg = sorted(las_inlagg(), key=lambda post: post["id"], reverse=True)
    return render_template(
        "index.html",
        inlagg=inlagg,
        fel=fel,
        formular=formular,
        tack=request.args.get("tack"),
        max_meddelande=MAX_MEDDELANDE,
    )


@app.template_filter("datum")
def formatera_datum(iso_tid):
    """Gör om '2026-10-01T15:04:00' till '1 okt 2026 kl. 15:04'."""
    manader = ["jan", "feb", "mar", "apr", "maj", "jun",
               "jul", "aug", "sep", "okt", "nov", "dec"]
    t = datetime.fromisoformat(iso_tid)
    return f"{t.day} {manader[t.month - 1]} {t.year} kl. {t:%H:%M}"


if __name__ == "__main__":
    app.run(debug=True)
