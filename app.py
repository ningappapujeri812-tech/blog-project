from flask import Flask, render_template, request, redirect
import sqlite3
import os

# ✅ SAFE IMPORT (NEW OPENAI)
from openai import OpenAI

app = Flask(__name__)

# ✅ API KEY
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_PATH = "db.sqlite3"

# ✅ Create DB if not exists
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)
    conn.close()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    db = get_db()
    posts = db.execute("SELECT * FROM posts").fetchall()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:id>")
def post(id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id=?", (id,)).fetchone()
    return render_template("post.html", post=post)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        db = get_db()
        db.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        db.commit()

        return redirect("/")

    return '''
    <h2>Add Blog</h2>
    <form method="post">
        <input name="title" placeholder="Title"><br><br>
        <textarea name="content" placeholder="Content"></textarea><br><br>
        <button>Add</button>
    </form>
    '''


# 🤖 AI BLOG GENERATOR (SAFE VERSION)
@app.route("/generate", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        topic = request.form["topic"]

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Write a SEO optimized blog post about: {topic}"}
                ]
            )

            content = response.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"

        title = topic

        db = get_db()
        db.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        db.commit()

        return redirect("/")

    return '''
    <h2>Generate AI Blog</h2>
    <form method="post">
        <input name="topic" placeholder="Enter topic"><br><br>
        <button>Generate Blog</button>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
