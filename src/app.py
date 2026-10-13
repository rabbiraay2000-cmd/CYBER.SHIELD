"""Cyber Shield dashboard: live graph stats + alerts. Run: python src/app.py"""
import sys
import os
import threading
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from flask import Flask, jsonify, render_template
import sniffer
from sniffer import start_live_capture

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder=os.path.join(BASE, "dashboard"))
graph = sniffer.graph  # same graph object the capture feeds


def capture_thread():
    try:
        start_live_capture()
    except Exception as e:
        print("Live capture unavailable:", e)


threading.Thread(target=capture_thread, daemon=True).start()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():
    return jsonify(graph.summary())


@app.route("/api/alerts")
def alerts():
    return jsonify([{"ip": ip, "type": k, "reason": r}
                    for ip, k, r in graph.detect()])


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "cyber-shield"})


@app.route("/api/graph")
def api_graph():
    threats = {ip: k for ip, k, _ in graph.detect()}
    nodes = [{"id": n, "in": graph.g.in_degree(n), "out": graph.g.out_degree(n),
              "threat": threats.get(n, "")} for n in graph.g.nodes]
    edges = [{"src": u, "dst": v, "w": d.get("weight", 1)}
             for u, v, d in graph.g.edges(data=True)]
    return jsonify({"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    app.run(host="0.0.0.0", port=port, debug=False)
