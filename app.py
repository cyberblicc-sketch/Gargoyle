from flask import Flask, jsonify, render_template, request, send_from_directory
from pathlib import Path

app = Flask(__name__)


def jurist(query: str):
    return {
        "source": "Jurist",
        "data": f"Legal analysis for '{query}': identify the main rules, filing risks, and compliance constraints."
    }


def cartographer(query: str):
    return {
        "source": "Cartographer",
        "data": f"Patent and market map for '{query}': identify adjacent opportunities and likely overlap areas."
    }


def strategist(query: str):
    return {
        "source": "Strategist",
        "data": f"Scenario simulation for '{query}': compare conservative, balanced, and aggressive paths."
    }


def run_demo(goal: str):
    return [jurist(goal), cartographer(goal), strategist(goal)]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/demo", methods=["POST"])
def demo():
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()
    if not query:
        return jsonify({"error": "query is required"}), 400
    return jsonify({"query": query, "results": run_demo(query)})


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.route("/docs/<path:filename>")
def docs_file(filename):
    return send_from_directory(Path(app.root_path) / "docs", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
