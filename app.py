from flask import Flask, render_template, request
import sqlite3
from ml_model import detect_leak

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/admin")
def admin():
    conn = sqlite3.connect("aquaguard.db")
    conn.row_factory = sqlite3.Row

    reports = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()

    conn.close()

    return render_template("admin.html", reports=reports)


# AI Prediction

@app.route("/ai", methods=["GET", "POST"])
def ai_prediction():
    result = None

    if request.method == "POST":
        pressure = float(request.form["pressure"])
        flow_rate = float(request.form["flow_rate"])

        result = detect_leak(pressure, flow_rate)

    return render_template("ai.html", result=result)




# Create database table
def create_table():

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            leak_type TEXT,
            severity TEXT,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save leakage report
def save_report(location, leak_type, severity, description):

    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports
        (location, leak_type, severity, description)
        VALUES (?, ?, ?, ?)
    """, (location, leak_type, severity, description))

    conn.commit()
    conn.close()


# Report Leakage
@app.route("/report", methods=["GET", "POST"])
def report():

    if request.method == "POST":

        location = request.form["location"]
        leak_type = request.form["leak_type"]
        severity = request.form["severity"]
        description = request.form["description"]

        save_report(
            location,
            leak_type,
            severity,
            description
        )

        return render_template(
            "report.html",
            message="✅ Leakage report saved successfully!"
        )

    return render_template("report.html")


# Run application
if __name__ == "__main__":

    create_table()

    app.run(debug=True)