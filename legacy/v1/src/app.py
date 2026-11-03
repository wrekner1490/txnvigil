"""
Live fraud-monitoring dashboard.

Replays the unseen test window as a transaction stream, scores each txn with the
trained model + rule engine, and pushes results to the browser with Server-Sent
Events (SSE). Alerts show risk score and reason codes, like an analyst queue.

Usage:  python src/app.py   ->  http://127.0.0.1:5000   (?speed=200 txns/sec)
"""
import json
import sys
import time
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, Response, render_template, request

sys.path.insert(0, str(Path(__file__).parent))
from explain import reason_codes
from rules import apply_rules

ROOT = Path(__file__).resolve().parents[1]
app = Flask(__name__, template_folder=str(ROOT / "templates"))
BUNDLE = joblib.load(ROOT / "reports" / "model.joblib")
STREAM = pd.read_pickle(ROOT / "data" / "stream.pkl").reset_index(drop=True)
F, THR = BUNDLE["features"], BUNDLE["threshold"]


def score_stream(speed: int, batch: int = 50):
    for i in range(0, len(STREAM), batch):
        chunk = STREAM.iloc[i:i + batch]
        s = BUNDLE["model"].predict_proba(chunk[F])[:, 1]
        rules = apply_rules(chunk)
        out = []
        for j, (_, r) in enumerate(chunk.iterrows()):
            fired = [c for c in rules.columns[:-1] if rules.iloc[j][c] == 1]
            alert = bool(s[j] >= THR or fired)
            ev = {"id": int(r.txn_id), "ts": str(r.ts)[:19], "user": int(r.user_id), "payee": int(r.payee_id),
                  "amount": float(r.amount), "channel": r.channel, "score": round(float(s[j]), 4),
                  "alert": alert, "is_fraud": int(r.is_fraud), "type": r.fraud_type}
            if alert:
                ev["rules"] = fired
                ev["reasons"] = reason_codes(r, BUNDLE)
            out.append(ev)
        yield f"data: {json.dumps(out)}\n\n"
        time.sleep(batch / speed)


@app.route("/")
def index():
    return render_template("dashboard.html", threshold=round(THR, 3))


@app.route("/stream")
def stream():
    speed = int(request.args.get("speed", 300))
    return Response(score_stream(speed), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


if __name__ == "__main__":
    app.run(debug=False, threaded=True)
