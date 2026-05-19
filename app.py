from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "db.sqlite3"

# Create DB if not exists
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


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
