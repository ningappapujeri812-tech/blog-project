import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# ✅ Set API Key from Render Environment
openai.api_key = os.getenv("OPENAI_API_KEY")


# ✅ Home Page
@app.route("/")
def home():
    return render_template("index.html")


# ✅ Generate Blog Route
@app.route("/generate", methods=["POST"])
def generate():
    try:
        topic = request.form.get("topic")

        if not topic:
            return "❌ Please enter a topic"

        # ✅ OpenAI API Call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Write a SEO optimized blog post about: {topic}"}
            ]
        )

        content = response["choices"][0]["message"]["content"]

        return render_template("result.html", content=content)

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ Run App (for local testing)
if __name__ == "__main__":
    app.run(debug=True)
@app.route("/add")
def add_post():
    return render_template("index.html")
