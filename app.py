from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "gmu_club.db"

# --- Initialize Database ---
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # Table for club members
        c.execute("""
            CREATE TABLE members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                reason TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table for events
        c.execute("""
            CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        # Table for projects
        c.execute("""
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        # Insert sample events
        c.executemany("INSERT INTO events (title, description, date) VALUES (?, ?, ?)", [
            ("Hackathon 2025", "24-hour coding marathon where innovation meets collaboration.", "Nov 12, 2025"),
            ("AI Workshop", "Hands-on session on Machine Learning with Python & TensorFlow.", "Dec 3, 2025"),
            ("Web Dev Bootcamp", "Learn to build interactive websites with HTML, CSS, and JS.", "Jan 15, 2026")
        ])
        # Insert sample projects
        c.executemany("INSERT INTO projects (title, description) VALUES (?, ?)", [
            ("Smart Campus App", "IoT-based campus automation and student engagement system."),
            ("AI Chatbot", "An intelligent chatbot for student queries using NLP."),
            ("Portfolio Builder", "A simple platform for students to create and host portfolios.")
        ])
        conn.commit()
        conn.close()

init_db()

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        reason = request.form.get("reason")
        if not name or not email or not reason:
            flash("All fields are required!", "error")
        else:
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO members (name, email, reason) VALUES (?, ?, ?)", (name, email, reason))
                conn.commit()
                conn.close()
                flash("🎉 Thank you for joining the GMU Coding Club!", "success")
                return redirect(url_for("home"))
            except sqlite3.IntegrityError:
                flash("Email already registered!", "error")

    # Fetch events & projects
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, description, date FROM events")
    events = c.fetchall()
    c.execute("SELECT title, description FROM projects")
    projects = c.fetchall()
    conn.close()

    # Quiz Data
    quiz_data = [
        {
            "question": "Which language is primarily used for web development?",
            "options": ["Python", "JavaScript", "C++", "Java"],
            "answer": "JavaScript"
        },
        {
            "question": "HTML stands for?",
            "options": ["Hyper Text Markup Language", "High Text Machine Language", "Hyperlink Text Management", "Home Tool Markup Language"],
            "answer": "Hyper Text Markup Language"
        },
        {
            "question": "CSS is used for?",
            "options": ["Content Structure", "Styling Web Pages", "Database Management", "Server-side scripting"],
            "answer": "Styling Web Pages"
        },
        {
            "question": "Which of these is a frontend framework?",
            "options": ["Django", "React", "Flask", "Laravel"],
            "answer": "React"
        }
    ]

    return render_template("index.html", events=events, projects=projects, quiz_data=quiz_data)


if __name__ == "__main__":
    app.run(debug=True)
