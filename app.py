from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "database/knowledge.db"

# データベース作成
def init_db():
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM knowledge ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    return render_template("index.html", data=data)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        content = request.form["content"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO knowledge(title, category, content) VALUES(?,?,?)",
            (title, category, content)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


@app.route("/detail/<int:id>")
def detail(id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM knowledge WHERE id=?", (id,))
    item = cursor.fetchone()

    conn.close()

    return render_template("detail.html", item=item)


if __name__ == "__main__":
    app.run(debug=True)
