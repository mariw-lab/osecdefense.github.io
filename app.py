from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__, static_folder=".")

@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.route("/trigger_payout", methods=["POST"])
def trigger_payout():
    data = request.json
    print("[PAYOUT TRIGGERED]", data)
    return jsonify({"status": "success", "message": "Live backend received payout trigger"})

@app.route("/ghostmint_inject", methods=["POST"])
def ghostmint_inject():
    print("[GHOSTMINT] Passive injection detected")
    return jsonify({"status": "ok", "message": "GhostMint logic acknowledged"})

@app.route("/vanish_logs", methods=["POST"])
def vanish_logs():
    print("[VANISH] Logs wiped (simulated)")
    return jsonify({"status": "vanished"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
