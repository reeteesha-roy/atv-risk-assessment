from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

def normalize_score(v):
    if isinstance(v, (int, float)): return int(v)
    return {"low":1, "medium":3, "high":5}.get(str(v).lower(), 3)

def normalize_confidence(v):
    if isinstance(v, (int, float)): return float(v)
    return {"low":0.3, "medium":0.6, "high":0.9}.get(str(v).lower(), 0.6)

def extract_json(text):
    start = text.find("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    df = pd.read_csv("atv_dataset.csv")
    df.ffill(inplace=True)

    prompt = f"""
You are an AI risk assessment engine for an eBAJA ATV manufacturing company.

Scenarios: Earthquake, Pandemic, War, Fire

DATA:
{df.to_json(orient="records")}

Return ONLY JSON ARRAY with:
scenario, risk_name, likelihood, impact, confidence, early_indicators, reason
"""

    res = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role":"system","content":"You are a professional enterprise risk analyst."},
            {"role":"user","content":prompt}
        ],
        temperature=0.3,
        max_tokens=900
    )

    risks = extract_json(res.choices[0].message.content)

    for r in risks:
        r["likelihood"] = normalize_score(r["likelihood"])
        r["impact"] = normalize_score(r["impact"])
        r["confidence"] = normalize_confidence(r["confidence"])
        r["score"] = round(r["likelihood"] * r["impact"] * r["confidence"], 2)

    risks = sorted(risks, key=lambda x: x["score"], reverse=True)
    return jsonify(risks)

if __name__ == "__main__":
    app.run(debug=True)
