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
        <style>
            body {
                font-family: 'Segoe UI';
                background: linear-gradient(135deg,#6a11cb,#2575fc);
                text-align:center;
                color:white;
            }
            .box {
                margin-top:100px;
            }
            a {
                display:inline-block;
                margin:10px;
                padding:12px 25px;
                background:#ff7eb3;
                color:white;
                text-decoration:none;
                border-radius:25px;
            }
            a:hover {background:#ff4e9b;}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🎓 Student Dashboard</h1>
            <a href="/add">➕ Add Student</a>
            <a href="/students">📋 View Students</a>
            <a href="/search">🔍 Search</a>
        </div>
    </body>
    </html>
    """

# ---------------- ADD ----------------
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        section = request.form['section']

        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name,grade,section) VALUES (?,?,?)",
                  (name,grade,section))
        conn.commit()
        conn.close()

        return redirect('/students')

    return """
    <html>
    <head>
        <style>
            body {
                font-family:Segoe UI;
                background:linear-gradient(135deg,#ff9a9e,#fad0c4);
                text-align:center;
            }
            .form-box {
                background:white;
                padding:30px;
                margin-top:80px;
                display:inline-block;
                border-radius:20px;
                box-shadow:0 5px 20px rgba(0,0,0,0.2);
            }
            input {
                margin:10px;
                padding:10px;
                width:220px;
                border-radius:10px;
                border:1px solid #ccc;
            }
            button {
                padding:10px 20px;
                border:none;
                border-radius:20px;
                background:#6a11cb;
                color:white;
                cursor:pointer;
            }
            button:hover {background:#2575fc;}
        </style>
    </head>
    <body>
        <div class="form-box">
            <h2>➕ Add Student</h2>
            <form method="POST">
                <input name="name" placeholder="Name" required><br>
                <input name="grade" placeholder="Grade" required><br>
                <input name="section" placeholder="Section" required><br>
                <button>Save</button>
            </form>
            <br><a href="/">⬅ Back</a>
        </div>
    </body>
    </html>
    """

# ---------------- VIEW ----------------
@app.route('/students')
def students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    data = c.execute("SELECT * FROM students").fetchall()
    conn.close()

    rows = ""
    for s in data:
        rows += f"""
        <tr>
            <td>{s[0]}</td>
            <td>{s[1]}</td>
            <td>{s[2]}</td>
            <td>{s[3]}</td>
            <td>
                <a href="/edit/{s[0]}">✏️</a>
                <a href="/delete/{s[0]}">❌</a>
            </td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family:Segoe UI;
                background:linear-gradient(135deg,#a18cd1,#fbc2eb);
                text-align:center;
            }}
            table {{
                margin:auto;
                margin-top:50px;
                border-collapse:collapse;
                background:white;
                border-radius:15px;
                overflow:hidden;
                box-shadow:0 5px 20px rgba(0,0,0,0.2);
            }}
            th, td {{
                padding:12px 20px;
                border-bottom:1px solid #ddd;
            }}
            th {{
                background:#6a11cb;
                color:white;
            }}
            tr:hover {{background:#f1f1f1;}}
            a {{
                text-decoration:none;
                margin:5px;
            }}
        </style>
    </head>
    <body>
        <h1>📋 Student Table</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Grade</th>
                <th>Section</th>
                <th>Action</th>
            </tr>
            {rows if rows else "<tr><td colspan='5'>No data</td></tr>"}
        </table>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/students')

# ---------------- EDIT ----------------
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        grade = request.form['grade']
        section = request.form['section']

        c.execute("UPDATE students SET name=?,grade=?,section=? WHERE id=?",
                  (name,grade,section,id))
        conn.commit()
        conn.close()
        return redirect('/students')

    student = c.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()

    return f"""
    <html>
    <body style="text-align:center;font-family:Segoe UI;">
        <h2>✏️ Edit Student</h2>
        <form method="POST">
            <input name="name" value="{student[1]}"><br><br>
            <input name="grade" value="{student[2]}"><br><br>
            <input name="section" value="{student[3]}"><br><br>
            <button>Update</button>
        </form>
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

        return f"<h1>Results</h1>{result}<a href='/'>Back</a>"

    return """
    <h2>🔍 Search</h2>
    <form method="POST">
        <input name="keyword">
        <button>Search</button>
    </form>
    """

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
    
