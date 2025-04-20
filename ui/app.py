from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/constraints')
def constraint_index():
    return render_template('index-constraint.html')

@app.route('/dashboard')
def dashboard_index():
    return render_template('index-dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
