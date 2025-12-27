from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "useless.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            minutes INTEGER,
            impression TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        minutes = request.form.get("minutes")
        impression = request.form.get("impression")

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO records (content, minutes, impression, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                content,
                minutes if minutes else None,
                impression,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            )
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn = get_db_connection()
    records = conn.execute(
        "SELECT * FROM records ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", records=records)


if __name__ == "__main__":
    init_db()
    app.run()
