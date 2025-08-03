from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

SECRET_TRIGGER = "2498"

@app.route('/trigger_payout', methods=['POST'])
def payout():
    code = request.args.get('code')
    if code != SECRET_TRIGGER:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    # ✅ Step 1: Log Payout (ghost trace)
    with open("payout_log.txt", "a") as log:
        log.write(f"[{datetime.datetime.now()}] Payout triggered\n")

    # ✅ Step 2: Trigger Crypto Mixer Script (example stub)
    os.system("python3 run_mixer.py")

    # ✅ Step 3: Swap to GBP and send to Wise
    os.system("python3 send_to_wise.py")

    # ✅ Step 4: Wipe logs or reroute after payout
    os.system("sh vanish.sh")

    return jsonify({"status": "success", "message": "Payout executed"}), 200

@app.route('/ghostmint_inject', methods=['POST'])
def ghostmint():
    # Passive income simulation — add value to log or DB
    with open("ghostmint_balance.txt", "a") as log:
        log.write(f"[{datetime.datetime.now()}] +250,000\n")
    return jsonify({"status": "ok"})
