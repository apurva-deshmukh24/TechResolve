
from flask import Flask, jsonify, send_from_directory

import os

from diagnostics import run_diagnostics

from database import (
    initialize_database,
    save_diagnostic,
    get_diagnostic_history
)


# Project Paths
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


# Initialize Flask
app = Flask(__name__)


# Initialize Database
initialize_database()


# Homepage
@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# Serve CSS and JavaScript
@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# API: Run Diagnostics
@app.route("/api/diagnostics", methods=["GET"])
def diagnostics():

    report = run_diagnostics()

    save_diagnostic(report)

    return jsonify(report)


# API: Diagnostic History
@app.route("/api/history", methods=["GET"])
def history():

    records = get_diagnostic_history()

    return jsonify(records)


# Start Application
if __name__ == "__main__":

    app.run(debug=True)
