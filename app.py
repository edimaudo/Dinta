import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

ORCHESTRATE_URL = os.getenv("ORCHESTRATE_URL")
ORCHESTRATE_API_KEY = os.getenv("ORCHESTRATE_API_KEY")


# ---------- Pages ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/app")
def app_page():
    return render_template("app.html")


# ---------- Orchestrate Call ----------

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    payload = {
        "problem": data.get("problem"),
        "assumptions": data.get("assumptions"),
        "framework": data.get("framework")
    }

    headers = {
        "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(ORCHESTRATE_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- 404 ----------

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
