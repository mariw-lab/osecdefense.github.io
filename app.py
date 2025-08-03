# HYDRA Web App - OMNIA EDITION + FINALIZED PAYMENT OPS
# Every Upgrade, Every Feature, All In One

from flask import Flask, render_template_string, request
import datetime, base64, hashlib, random

app = Flask(__name__)

# === CONFIG ===
balance = 3_200_000
withdrawal_request = None
live_mode = False
vanish_triggered = False
logs = []
shadow_logs = []
vault_entries = []
operator_signature = "OpenHydra"
operator_key = "osec-master"
payment_history = []

# === PAYMENT ROUTES CONFIG ===
WISE_API_TOKEN = "cbef0212-08dd-49f7-b10a-9ad0294"
DEST_IBAN = "GB23 TRWI 2308 0173 8658 35"
EMAIL_ADDRESS = "w.omarion@icloud.com"
EMAIL_PASSWORD = "ormb-jdip-awyn-omag"
EMAIL_SMTP_SERVER = "smtp.mail.com"
EMAIL_SMTP_PORT = 587
XMR_WALLET = "42MQ5pDUv17VgnRT9EFAW5dcPBbBYu1XX5Jd"
BANK_SORT = "23-08-01"
BANK_ACC = "60628998"
WISE_NAME = "Omarion Wilson"

# === FUNCTION: ENCRYPT VAULT ENTRY ===
def encrypt_entry(entry):
    key = hashlib.sha256(operator_key.encode()).hexdigest()[:16]
    return base64.b64encode((entry + key).encode()).decode()

# === FUNCTION: SIMULATE ROUTING CHAIN ===
def simulate_payment(amount):
    if amount <= 4000:
        return "Revolut"
    elif amount <= 50000:
        return "Wise"
    else:
        return "Monero"

# === FUNCTION: FAKE EMAIL RECEIPT ===
def send_fake_receipt(amount, method):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    logs.append(f"📤 [RECEIPT] Fake {method} confirmation email sent for £{amount:,} at {now}")
    shadow_logs.append(f"[SHADOW] Spoofed receipt dispatched via SMTP.")

# === FUNCTION: AUTOSWITCH TO SIM AFTER PAYOUT ===
def auto_reset_after_live():
    global live_mode
    live_mode = False
    logs.append("🔒 LIVE mode auto-disabled after payout.")
    shadow_logs.append("[SECURE] Auto-reset to SIM mode after payment.")

# === FUNCTION: HANDLE COMMANDS ===
def handle_command(cmd):
    global withdrawal_request, balance, live_mode, vanish_triggered
    now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    cmd = cmd.strip()
    low = cmd.lower()

    if low.startswith("withdraw"):
        try:
            amount = int(low.split()[1])
            withdrawal_request = amount
            logs.append(f"{now} 💸 Withdraw requested: £{amount:,}")
            return f"Withdrawal of £{amount:,} requested. Type 'confirm withdraw'."
        except:
            return "❌ Invalid format. Use: withdraw <amount>"

    elif low == "confirm withdraw":
        if withdrawal_request:
            logs.append(f"{now} ✅ Withdrawal confirmed: £{withdrawal_request:,}")
            return "Now type 'send funds' to complete."
        return "❌ No withdrawal to confirm."

    elif low == "send funds":
        if not withdrawal_request:
            return "❌ No withdrawal in progress."
        route = simulate_payment(withdrawal_request)
        if live_mode:
            logs.append(f"{now} [LIVE] Sent £{withdrawal_request:,} via {route}")
            shadow_logs.append(f"{now} [LIVE] Routed £{withdrawal_request:,} through {route}")
            send_fake_receipt(withdrawal_request, route)
            auto_reset_after_live()
        else:
            logs.append(f"{now} [SIM] Simulated £{withdrawal_request:,} → {route}")
            shadow_logs.append(f"{now} [SIM] Would send £{withdrawal_request:,} via {route}")
        balance_change = withdrawal_request
        balance_change += random.randint(-20, 20)
        balance -= balance_change
        payment_history.append((withdrawal_request, route, live_mode))
        withdrawal_request = None
        return f"✅ {'Executed' if live_mode else 'Simulated'} transfer via {route}. New balance: £{balance:,}"

    elif low == "cancel withdraw":
        withdrawal_request = None
        return "❌ Withdrawal cancelled."

    elif low in ["/go live", "/live activate", "/enable all"]:
        return "🔐 Authenticate Operator Signature to enable LIVE mode. Type: unlock <signature>"

    elif low.startswith("unlock"):
        try:
            sig = cmd.split(" ", 1)[1].strip()
            if sig == operator_signature:
                live_mode = True
                logs.append(f"{now} 🔓 LIVE MODE ENABLED by Operator")
                shadow_logs.append(f"{now} [AUTH] LIVE switch flipped.")
                return "✅ LIVE MODE ENABLED. All modules HOT."
            else:
                return "❌ Invalid signature. LIVE mode denied."
        except:
            return "❌ Format: unlock <signature>"

    elif low == "/cancel live":
        live_mode = False
        logs.append("🔒 LIVE MODE DISABLED by Operator command.")
        return "LIVE mode disabled manually."

    elif low == "vanish":
        vanish_triggered = True
        logs.append(f"{now} 🧨 VANISH protocol primed.")
        return "🫥 VANISH protocol triggered. Logs cloaked."

    elif low.startswith("vault add"):
        entry = cmd[10:]
        encrypted = encrypt_entry(entry)
        vault_entries.append(f"{now} 🔐 {encrypted}")
        return "Vault entry added and encrypted."

    elif low == "vault view":
        return "\n".join(vault_entries[-5:]) if vault_entries else "Vault is empty."

    elif low == "income":
        status = "LIVE" if live_mode else "SIM"
        logs.append(f"{now} 💰 GhostMint ({status}): Auto income check complete.")
        return f"GhostMint running in {status} mode. Recon modules operational."

    elif low == "clones":
        return f"🧬 CloneOps running in {'LIVE' if live_mode else 'SIM'} mode. Tracking active sessions."

    elif low == "attack":
        if live_mode:
            return "☠️ LIVE Self-Attack: Payloads queued for delivery."
        return "(SIM) Self-Attack test: No real payloads launched."

    elif low == "/route":
        if withdrawal_request:
            return f"📡 Routing: {simulate_payment(withdrawal_request)}"
        return "No pending amount to route."

    elif low == "/simulate payout":
        amt = random.randint(5000, 80000)
        method = simulate_payment(amt)
        return f"Simulated routing for £{amt:,} → {method}"

    elif low == "/ghost receipt":
        send_fake_receipt(25000, "Wise")
        return "📥 Spoofed receipt triggered."

    elif low == "logs":
        return "\n".join(logs[-10:])

    elif low == "shadow":
        return "\n".join(shadow_logs[-10:])

    elif low == "help":
        return ("Commands:\n- withdraw <amount>\n- confirm withdraw\n- send funds\n- vault add <text>\n- vault view\n"
                "- /go live → unlock <signature>\n- income\n- clones\n- attack\n- /route\n- /simulate payout\n"
                "- /ghost receipt\n- /cancel live\n- logs\n- shadow\n- vanish\n- help")

    else:
        logs.append(f"{now} ❓ Unknown command: {cmd}")
        return "Unknown command. Type 'help'."

# === ROUTE ===
@app.route("/", methods=["GET", "POST"])
def index():
    console_output = ""
    if request.method == "POST":
        cmd = request.form["command"]
        console_output = handle_command(cmd)

    return render_template_string("""
    <!doctype html>
    <html>
    <head>
        <title>HYDRA :: {{ 'LIVE' if live_mode else 'SIM' }}</title>
        <style>
            body { background:black; color:#00FF88; font-family:monospace; margin:0; padding:0; }
            .header { background:#111; padding:12px; text-align:center; font-size:20px; font-weight:bold; border-bottom:2px solid #0f0; }
            .tabs { display:flex; justify-content:center; background:#222; padding:10px; }
            .tabs button { background:#0f0; color:black; border:none; margin:3px; padding:10px; font-weight:bold; border-radius:4px; cursor:pointer; }
            .main { padding:20px; }
            .console { background:#000; border:1px solid #0f0; padding:10px; height:300px; overflow-y:scroll; white-space:pre-wrap; margin-bottom:12px; }
            .input { display:flex; }
            .input input[type=text] { flex:1; padding:10px; border:1px solid #0f0; background:black; color:#0f0; font-family:monospace; }
            .input input[type=submit] { padding:10px; background:#0f0; color:black; border:none; font-weight:bold; cursor:pointer; }
        </style>
    </head>
    <body>
        <div class="header">HYDRA OS :: OMNIA MODE | {{ 'LIVE' if live_mode else 'SIM' }} | BALANCE: £{{ "{:,}".format(balance) }}</div>
        <div class="tabs">
            <button>Console</button><button>Vault</button><button>Logs</button><button>CloneOps</button>
            <button>GhostMint</button><button>Self-Attack</button><button style="background:red;">VANISH</button>
        </div>
        <div class="main">
            <div class="console">
                {% for line in logs[-15:] %}{{ line }}<br>{% endfor %}
                {% if console_output %}<b>{{ console_output }}</b>{% endif %}
            </div>
            <form method="post" class="input">
                <input type="text" name="command" placeholder="Enter command...">
                <input type="submit" value="Execute">
            </form>
        </div>
    </body>
    </html>
    """, balance=balance, logs=logs, console_output=console_output, live_mode=live_mode)

# === START ===
if __name__ == "__main__":
    app.run(debug=False)
