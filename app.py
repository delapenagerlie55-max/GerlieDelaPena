from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade TEXT,
            section TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>My Flask API</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: white;
                text-align: center;
            }
            .container {
                margin-top: 100px;
                padding: 30px;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                display: inline-block;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .btn {
                margin: 10px;
                padding: 12px 25px;
                border: none;
                border-radius: 30px;
                background: #ff7eb3;
                color: white;
                font-size: 16px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover {
                background: #ff4e9b;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 Welcome to My Flask API</h1>
            <p>Student System Dashboard</p>

            <a href="/add" class="btn">➕ Add Student</a>
            <a href="/students" class="btn">📋 View Students</a>
            <a href="/search" class="btn">🔍 Search</a>
        </div>
    </body>
    </html>
    """

# ---------------- ADD STUDENT ----------------
@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        section = request.form['section']

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, grade, section) VALUES (?, ?, ?)",
                  (name, grade, section))
        conn.commit()
        conn.close()

        return redirect('/students')

    return """
    <html>
    <body style="font-family:Segoe UI; text-align:center; background:#fad0c4;">
        <h2>➕ Add Student</h2>
        <form method="POST">
            <input name="name" placeholder="Name" required><br><br>
            <input name="grade" placeholder="Grade" required><br><br>
            <input name="section" placeholder="Section" required><br><br>
            <button>Save</button>
        </form>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

# ---------------- VIEW STUDENTS ----------------
@app.route('/students')
def students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    data = c.execute("SELECT * FROM students").fetchall()
    conn.close()

    cards = ""
    for s in data:
        cards += f"""
        <div style='background:white; margin:10px; padding:15px; border-radius:15px;'>
            <p><b>Name:</b> {s[1]}</p>
            <p><b>Grade:</b> {s[2]}</p>
            <p><b>Section:</b> {s[3]}</p>
        </div>
        """

    return f"""
    <html>
    <body style="font-family:Segoe UI; text-align:center; background:#a18cd1;">
        <h1>📋 Student List</h1>
        {cards if cards else "<p>No students yet</p>"}
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

# ---------------- SEARCH ----------------
@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        data = c.execute("SELECT * FROM students WHERE name LIKE ?",
                         ('%'+keyword+'%',)).fetchall()
        conn.close()

        result = ""
        for s in data:
            result += f"<p>{s[1]} - Grade {s[2]}</p>"

        return f"""
        <h1>🔍 Results</h1>
        {result if result else "<p>No match found</p>"}
        <a href="/">⬅ Back</a>
        """

    return """
    <html>
    <body style="font-family:Segoe UI; text-align:center;">
        <h2>🔍 Search Student</h2>
        <form method="POST">
            <input name="keyword" placeholder="Enter name">
            <button>Search</button>
        </form>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
    
