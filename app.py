# ─────────────────────────────────────────────
#  DataNarrate - Simple Version
#  Flask backend with SQLite database
# ─────────────────────────────────────────────

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
from datetime import datetime

# Create the Flask app
app = Flask(__name__)

DB = "datanarrate.db"

def init_db():
    ...

def seed():
    ...

init_db()
seed()

# ── CREATE DATABASE TABLES ──────────────────
def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT,
            category   TEXT,
            chart_type TEXT,
            raw_data   TEXT,
            insights   TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# ── GENERATE INSIGHTS FROM DATA ─────────────
def get_insights(rows):
    # rows = list of {"label": "...", "value": 123}

    values = [r["value"] for r in rows]
    labels = [r["label"] for r in rows]

    total   = sum(values)
    average = round(total / len(values), 2)
    highest = max(values)
    lowest  = min(values)

    top_label = labels[values.index(highest)]
    low_label = labels[values.index(lowest)]
    top_share = round((highest / total) * 100, 1)

    # Simple trend: compare first half vs second half
    mid        = len(values) // 2
    first_avg  = sum(values[:mid]) / mid if mid > 0 else 0
    second_avg = sum(values[mid:]) / (len(values) - mid)

    if second_avg > first_avg * 1.1:
        trend = "an upward trend "
    elif second_avg < first_avg * 0.9:
        trend = "a downward trend "
    else:
        trend = "a stable trend "

    # Return list of insight sentences
    return [
        f"<b>{top_label}</b> has the highest value of <b>{highest:,}</b>, making up {top_share}% of the total.",
        f"There are <b>{len(values)}</b> data points. Total = <b>{total:,}</b>, Average = <b>{average:,}</b>.",
        f"<b>{low_label}</b> has the lowest value at <b>{lowest:,}</b>.",
        f"The data shows <b>{trend}</b> overall."
    ]


# ── PARSE USER INPUT INTO ROWS ───────────────
def parse_data(text):
    rows = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Support both comma and colon separators
        if "," in line:
            parts = line.split(",", 1)
        elif ":" in line:
            parts = line.split(":", 1)
        else:
            continue
        try:
            label = parts[0].strip()
            value = float(parts[1].strip())
            rows.append({"label": label, "value": value})
        except ValueError:
            continue  # skip bad lines
    return rows


# ── SEED DEMO DATA ───────────────────────────
def seed():
    conn = sqlite3.connect(DB)
    count = conn.execute("SELECT COUNT(*) FROM stories").fetchone()[0]
    conn.close()

    if count > 0:
        return  # already has data

    demos = [
        ("Q4 Sales by Region",     "sales",   "bar",
         "North America,420000\nEurope,310000\nAsia,280000\nLatin America,190000"),

        ("Student Survey Results", "survey",  "pie",
         "Excellent,312\nGood,285\nAverage,198\nPoor,34"),

        ("Monthly Website Traffic","custom",  "line",
         "January,18200\nFebruary,21400\nMarch,19800\nApril,24100\nMay,28700"),

        ("Department Budget",      "finance", "doughnut",
         "Engineering,450000\nMarketing,280000\nHR,120000\nOperations,200000"),
    ]

    conn = sqlite3.connect(DB)
    for title, cat, chart, raw in demos:
        rows     = parse_data(raw)
        insights = get_insights(rows)
        conn.execute(
            "INSERT INTO stories (title,category,chart_type,raw_data,insights,created_at) VALUES (?,?,?,?,?,?)",
            (title, cat, chart, json.dumps(rows), json.dumps(insights),
             datetime.now().strftime("%d %b %Y"))
        )
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════

# HOME PAGE
@app.route("/")
def home():
    conn    = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    stories = conn.execute(
        "SELECT * FROM stories ORDER BY id DESC LIMIT 6"
    ).fetchall()
    conn.close()
    return render_template("index.html", stories=stories)


# CREATE STORY PAGE
@app.route("/create")
def create():
    return render_template("create.html")


# HANDLE FORM SUBMIT
@app.route("/submit", methods=["POST"])
def submit():
    title      = request.form.get("title", "").strip()
    category   = request.form.get("category", "").strip()
    chart_type = request.form.get("chart_type", "bar").strip()
    raw_text   = request.form.get("raw_data", "").strip()

    # Server-side validation
    error = None
    if not title:
        error = "Please enter a title."
    elif not category:
        error = "Please select a category."
    elif not raw_text:
        error = "Please enter some data."

    rows = parse_data(raw_text)
    if not error and len(rows) < 2:
        error = "Please enter at least 2 valid rows (Label, Value)."

    if error:
        return render_template("create.html", error=error)

    # Generate insights
    insights = get_insights(rows)

    # Save to database
    conn = sqlite3.connect(DB)
    cur  = conn.execute(
        "INSERT INTO stories (title,category,chart_type,raw_data,insights,created_at) VALUES (?,?,?,?,?,?)",
        (title, category, chart_type, json.dumps(rows), json.dumps(insights),
         datetime.now().strftime("%d %b %Y"))
    )
    story_id = cur.lastrowid
    conn.commit()
    conn.close()

    return redirect(url_for("result", story_id=story_id))


# RESULT / STORY DETAIL PAGE
@app.route("/result/<int:story_id>")
def result(story_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    story = conn.execute(
        "SELECT * FROM stories WHERE id = ?", (story_id,)
    ).fetchone()
    conn.close()

    if not story:
        return redirect(url_for("home"))

    data     = json.loads(story["raw_data"])
    insights = json.loads(story["insights"])
    return render_template("result.html", story=story, data=data, insights=insights)


# GALLERY PAGE
@app.route("/gallery")
def gallery():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    stories = conn.execute(
        "SELECT * FROM stories ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("gallery.html", stories=stories)


# DELETE A STORY
@app.route("/delete/<int:story_id>", methods=["POST"])
def delete(story_id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM stories WHERE id = ?", (story_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("gallery"))


# ── RUN THE APP ──────────────────────────────
if __name__ == "__main__":
    init_db()   # create tables if not exist
    seed()      # add demo data if empty
    app.run(debug=True)
