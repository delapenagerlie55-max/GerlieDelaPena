from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>My Colorful Flask API</title>
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
                animation: fadeIn 1.5s ease-in-out;
            }
            h1 {
                font-size: 40px;
                margin-bottom: 10px;
            }
            p {
                font-size: 18px;
            }
            .btn {
                margin-top: 20px;
                padding: 12px 25px;
                border: none;
                border-radius: 30px;
                background: #ff7eb3;
                color: white;
                font-size: 16px;
                cursor: pointer;
                transition: 0.3s;
            }
            .btn:hover {
                background: #ff4e9b;
                transform: scale(1.05);
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(20px);}
                to {opacity: 1; transform: translateY(0);}
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 Welcome to My Flask API</h1>
            <p>Click below to view student information</p>
            <a href="/student">
                <button class="btn">View Student</button>
            </a>
        </div>
    </body>
    </html>
    """

@app.route('/student')
def get_student():
    return """
    <html>
    <head>
        <title>Student Info</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                color: #333;
                text-align: center;
            }
            .card {
                margin-top: 100px;
                padding: 30px;
                border-radius: 20px;
                background: white;
                display: inline-block;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                animation: pop 0.8s ease;
            }
            h2 {
                color: #ff4e9b;
            }
            p {
                font-size: 18px;
                margin: 10px 0;
            }
            .back {
                margin-top: 20px;
                display: inline-block;
                padding: 10px 20px;
                border-radius: 25px;
                background: #6a11cb;
                color: white;
                text-decoration: none;
                transition: 0.3s;
            }
            .back:hover {
                background: #2575fc;
            }
            @keyframes pop {
                from {transform: scale(0.7); opacity: 0;}
                to {transform: scale(1); opacity: 1;}
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🎓 Student Information</h2>
            <p><strong>Name:</strong> Your Name</p>
            <p><strong>Grade:</strong> 10</p>
            <p><strong>Section:</strong> Zechariah</p>
            <a href="/" class="back">⬅ Back Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
