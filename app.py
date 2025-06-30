from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import openai
import re

app = Flask(__name__)
app.secret_key = "secret123"  ###
openai.api_key = "*******"  # replace with your API key

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "pass123":
            session["admin"] = True
            return redirect("/admin")
        else:
            error = "❌ Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

#admin_panel
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        data = (
            request.form["title"],
            request.form["genre"],
            request.form["year"],
            request.form["rating"],
            request.form["poster_url"]
        )
        conn = sqlite3.connect("database/movies.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO movies (title, genre, year, rating, poster_url) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    return render_template("admin.html")


def get_movies():
    conn = sqlite3.connect("database/movies.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    conn.close()
    return movies


@app.route("/")
def index():
    movies = get_movies()
    return render_template("index.html", movies=movies)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    user_input = request.json["message"]

    genre = re.search(r"(action|romantic|comedy|horror|drama|sci-fi)", user_input, re.IGNORECASE)
    genre = genre.group(0).lower() if genre else ""
    year_match = re.search(r"(20\d{2})", user_input)
    year = int(year_match.group(1)) if year_match else 2000
    rating_match = re.search(r"rating.*?(\d+(\.\d+)?)", user_input)
    rating = float(rating_match.group(1)) if rating_match else 0

    conn = sqlite3.connect("database/movies.db")
    cur = conn.cursor()
    query = "SELECT title, genre, year, rating FROM movies WHERE 1=1"
    params = []

    if genre:
        query += " AND genre LIKE ?"
        params.append(f"%{genre}%")
    if year:
        query += " AND year >= ?"
        params.append(year)
    if rating:
        query += " AND rating >= ?"
        params.append(rating)

    cur.execute(query, params)
    results = cur.fetchall()
    conn.close()

    if not results:
        return jsonify({"reply": "Sorry, I couldn’t find any matching movies in the database."})

    movie_list = "\n".join([f"{title} ({year}) - {genre}, ⭐{rating}" for title, genre, year, rating in results[:10]])

    prompt = f"The user said: '{user_input}'. From this list, recommend some movies:\n\n{movie_list}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"reply": response.choices[0].message["content"]})

if __name__ == "__main__":
    app.run(debug=True)
