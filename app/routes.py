from app import app
from flask import render_template

@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")

@app.route("/")
def main():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()
