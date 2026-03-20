from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gargoyle | AI Shadow Consultant</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: Arial, sans-serif;
      background: #08111c;
      color: #f8fafc;
      line-height: 1.6;
    }
    .hero {
      min-height: 70vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 40px 20px;
      background: linear-gradient(180deg, #0f172a 0%, #08111c 100%);
    }
    .hero-inner {
      max-width: 850px;
    }
    h1 {
      font-size: 3rem;
      margin-bottom: 16px;
    }
    .tagline {
      font-size: 1.2rem;
      color: #cbd5e1;
      margin-bottom: 24px;
    }
    .btn {
      display: inline-block;
      background: #7c3aed;
      color: white;
      padding: 14px 22px;
      border-radius: 10px;
      text-decoration: none;
      font-weight: bold;
      border: none;
      cursor: pointer;
    }
    section {
      max-width: 1100px;
      margin: 0 auto;
      padding: 56px 20px;
    }
    h2 {
      text-align: center;
      margin-bottom: 24px;
      font-size: 2rem;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px;
    }
    .card {
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 14px;
      padding: 20px;
    }
    .card h3 {
      color: #a78bfa;
      margin-bottom: 10px;
    }
    .price {
      font-size: 1.8rem;
      color: #facc15;
      margin-bottom: 10px;
    }
    form {
      max-width: 800px;
      margin: 0 auto;
      display: grid;
      gap: 14px;
    }
    textarea {
      width: 100%;
      min-height: 150px;
      padding: 14px;
      border-radius: 10px;
      border: 1px solid #334155;
      background: #020617;
      color: #fff;
      font: inherit;
    }
    .result {
      max-width: 800px;
      margin: 24px auto 0;
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 14px;
      padding: 20px;
      white-space: pre-wrap;
    }
    .muted {
      color: #cbd5e1;
    }
    @media (max-width: 640px) {
      h1 { font-size: 2.2rem; }
      .tagline { font-size: 1rem; }
    }
  </style>
</head>
<body>
  <section class="hero">
    <div class="hero-inner">
      <h1>Master the Maze.</h1>
      <p class="tagline">
        Gargoyle is an AI-powered web service for legal, regulatory, patent, and strategic analysis.
      </p>
      <a class="btn" href="#demo">Run Demo</a>
    </div>
  </section>

  <section>
    <h2>Why Gargoyle</h2>
    <div class="grid">
      <div class="card">
        <h3>Jurist</h3>
        <p class="muted">Structured legal and regulatory analysis for filings, obligations, and compliance risks.</p>
      </div>
      <div class="card">
        <h3>Cartographer</h3>
        <p class="muted">Patent and market mapping to identify whitespace, overlap, and adjacent opportunities.</p>
      </div>
      <div class="card">
        <h3>Strategist</h3>
        <p class="muted">Scenario planning that compares conservative, balanced, and aggressive paths.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>Pricing</h2>
    <div class="grid">
      <div class="card">
        <h3>Starter</h3>
        <div class="price">$29/mo</div>
        <p class="muted">Jurist + Cartographer</p>
      </div>
      <div class="card">
        <h3>Pro</h3>
        <div class="price">$59/mo</div>
        <p class="muted">Adds Strategist and unlimited projects</p>
      </div>
      <div class="card">
        <h3>Enterprise</h3>
        <div class="price">Custom</div>
        <p class="muted">Dedicated environment and integrations</p>
      </div>
    </div>
  </section>

  <section id="demo">
    <h2>Interactive Demo</h2>
    <form id="demo-form">
      <textarea id="query" placeholder="How should a fintech startup reduce regulatory friction when launching in multiple states?"></textarea>
      <button class="btn" type="submit">Run analysis</button>
    </form>
    <div id="result" class="result" style="display:none;"></div>
  </section>

  <script>
    const form = document.getElementById("demo-form");
    const result = document.getElementById("result");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const query = document.getElementById("query").value.trim();

      if (!query) {
        alert("Please enter a query.");
        return;
      }

      result.style.display = "block";
      result.textContent = "Running demo...";

      try {
        const res = await fetch("/api/demo", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query })
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || "Request failed");
        }

        result.textContent = data.results.map(
          item => "- " + item.source + ": " + item.data
        ).join("\\n\\n");
      } catch (err) {
        result.textContent = "Error: " + err.message;
      }
    });
  </script>
</body>
</html>
"""

def jurist(query: str):
    return {
        "source": "Jurist",
        "data": f"Legal analysis for '{query}': identify the key rules, filing risks, and compliance constraints."
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

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/demo", methods=["POST"])
def demo():
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()
    if not query:
      return jsonify({"error": "query is required"}), 400

    return jsonify({
        "query": query,
        "results": [jurist(query), cartographer(query), strategist(query)]
    })

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
