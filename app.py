
import os
import json
import logging
from uuid import uuid4
from flask import Flask, render_template, request, jsonify, abort
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
logging.basicConfig(level=logging.INFO)

# Configuration: set these in your environment (or in a .env file)
ORCHESTRATE_URL = os.getenv("ORCHESTRATE_URL")      # e.g. https://api.ibm.com/...
ORCHESTRATE_API_KEY = os.getenv("ORCHESTRATE_API_KEY")  # set in env; used in Authorization header if required

# ---------- Routes ----------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/app")
def app_page():
    # Provide an app_id to the template (used by the client JS)
    return render_template("app.html", app_id=str(uuid4()))

# Endpoint expected by the client-side function callGeminiProxy()
# The original JS posts an object that includes systemInstruction and contents.
# We forward that input to Orchestrate (or simulate if not configured).
@app.route("/api/gemini-proxy", methods=["POST"])
def gemini_proxy():
    payload = request.get_json() or {}
    logging.info("gemini-proxy payload received")

    # If you want the JS to receive a Google-like "candidates" structure,
    # we return a similar shaped object so the existing client JS can parse JSON.
    try:
        if ORCHESTRATE_URL and ORCHESTRATE_API_KEY:
            # Build the Orchestrate request payload according to your workflow
            orchestrate_payload = {
                "input": payload,
                "meta": {"source": "gemini-proxy"}
            }
            headers = {
                "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
                "Content-Type": "application/json"
            }
            resp = requests.post(ORCHESTRATE_URL, json=orchestrate_payload, headers=headers, timeout=30)
            resp.raise_for_status()
            orchestrate_resp = resp.json()

            # The client expects structure: { candidates: [ { content: { parts: [ { text: "..." } ] } } ] }
            text_payload = json.dumps(orchestrate_resp)
            return jsonify({"candidates": [{"content": {"parts": [{"text": text_payload}]}}]})
        else:
            # Mock response (useful for local dev)
            simulated = {
                "analyses": [
                    {
                        "framework_name": "SWOT",
                        "why_selected": "Auto-selected for illustrative purposes.",
                        "decision": "Example decision.",
                        "sections": [{"title": "Example", "insights": ["Insight A", "Insight B"]}]
                    }
                ]
            }
            return jsonify({"candidates": [{"content": {"parts": [{"text": json.dumps(simulated)}]}}]})
    except Exception as e:
        logging.exception("Error in gemini_proxy")
        return jsonify({"error": str(e)}), 500

# Endpoint expected by handleNext() -> '/api/generate_analysis'
# This endpoint returns `{ success: true, analysisData: { analysisTitle, keyFindings: [...] } }`
@app.route("/api/generate_analysis", methods=["POST"])
def generate_analysis():
    payload = request.get_json() or {}
    logging.info("generate_analysis called")

    try:
        # Build the orchestrate input (this is what your workflow should accept)
        orchestrate_payload = {
            "problem": payload.get("problemStatement") or payload.get("userQuery") or payload.get("userQuery", ""),
            "assumptions": payload.get("assumptions") or "",
            "frameworks": payload.get("selectedFrameworks") or payload.get("framework") or "auto",
            "meta": {"caller": "generate_analysis"}
        }

        if ORCHESTRATE_URL and ORCHESTRATE_API_KEY:
            headers = {
                "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
                "Content-Type": "application/json",
            }
            resp = requests.post(ORCHESTRATE_URL, json=orchestrate_payload, headers=headers, timeout=30)
            resp.raise_for_status()
            orchestrate_resp = resp.json()

            # Transform Orchestrate response into the expected UI shape.
            # Expect orchestrate_resp to contain the merged outputs of Skills 1-4 & 6.
            analysisData = {
                "analysisTitle": orchestrate_resp.get("solution", {}).get("recommended_direction", "Strategic Analysis"),
                "keyFindings": orchestrate_resp.get("solution", {}).get("key_decisions", orchestrate_resp.get("framework_output", {}).get("insights", []))
            }
            return jsonify({"success": True, "analysisData": analysisData})
        else:
            # Mocked analysis data for local testing / demo without Orchestrate
            mock = {
                "analysisTitle": "Mock Analysis: Auto-selected SWOT",
                "keyFindings": [
                    "Strength: Clear product-market fit in niche",
                    "Weakness: Limited go-to-market budget",
                    "Opportunity: Quick partnership with local channels",
                    "Threat: New competitor with aggressive pricing"
                ]
            }
            return jsonify({"success": True, "analysisData": mock})
    except Exception as e:
        logging.exception("generate_analysis failed")
        return jsonify({"success": False, "error": str(e)}), 500


# A convenience POST endpoint that your simplified UI might call (optional)
@app.route("/analyze", methods=["POST"])
def analyze_simple():
    body = request.get_json() or {}
    problem = body.get("problem", "")
    assumptions = body.get("assumptions", "")
    framework = body.get("framework", "auto")

    # Use the same orchestrate call implementation as above
    # For simplicity return the combined mocked result
    result = {
        "problem_structuring": {
            "summary": problem[:300] if problem else "No problem provided.",
            "stakeholders": [],
            "constraints": []
        },
        "selected_framework": framework if framework != "auto" else "SWOT",
        "framework_analysis": {},
        "solution_synthesis": {},
        "execution_plan": [
            "Step 1: Create repo",
            "Step 2: Implement minimal pipeline",
            "Step 3: Validate with 3 users"
        ],
        "starter_code": "def main():\n    print('Hello Dinta')"
    }
    return jsonify(result)

# 404 handler rendering a simple page if route incorrect
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Entrypoint for local run (Vercel will use its own runner)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG", "0") == "1")
