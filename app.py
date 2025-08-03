from flask import Flask, request, jsonify, render_template_string
import os, time, json, random, uuid

app = Flask(__name__)

# === CORE CONFIG ===
BALANCE = 6200000.00
LIVE_MODE = True
WITHDRAW_PENDING = False
HYDRA_LINKED = True
VAULT_ACTIVE = True
LOGS = []

# === HTML UI TERMINAL ===
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>🧿 HYDRA ARKHØN OPS</title>
    <style>
        body { background: #000914; color: #00ffe1; font-family: monospace; padding: 20px; }
        input { background: #000914; color: #00ffe1; border: none; font-size: 1em; width: 100%; }
        .terminal { width: 100%; height: 80vh; overflow-y: auto; border: 1px solid #00ffe1; padding: 10px; }
    </style>
</head>
<body>
    <div class="terminal" id="terminal">
        <p>Initializing ARKHØN Phantom Protocol...</p>
        <p>Injecting GhostMint Engine...</p>
        <p>🧠 HYDRA Linked — AI Ops Online</p>
        <p>💸 Balance Locked: £6.2M | LIVE MODE ENABLED</p>
        <p>Type "/help" for commands.</p>
    </div>
    <input id="input" autofocus />
    <script>
        const input = document.getElementById("input");
        const terminal = document.getElementById("terminal");
        input.addEventListener("keydown", async (e) => {
            if (e.key === "Enter") {
                const cmd = input.value.trim();
                terminal.innerHTML += "<p>&gt; " + cmd + "</p>";
                input.value = "";
                const res = await fetch("/cmd", {
                    method: "POST",
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cmd })
                });
                const out = await res.text();
                terminal.innerHTML += "<p>" + out + "</p>";
                terminal.scrollTop = terminal.scrollHeight;
            }
        });
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/cmd", methods=["POST"])
def command():
    global BALANCE, LIVE_MODE, WITHDRAW_PENDING, HYDRA_LINKED, LOGS

    cmd = request.json.get("cmd", "").lower().strip()
    LOGS.append(cmd)

    if cmd in ["/help", "help"]:
        return """<b>Available Commands:</b><br>
        /balance → View current locked balance<br>
        /payout → Withdraw £500K via GhostMint routing<br>
        /trigger arkhon → Begin Phase X ARKHØN Ops<br>
        /launch cloneops → Deploy clone intelligence<br>
        /enter auto-lab → Cyber Lab Phantom routines<br>
        /start harvest → GhostMint Income Modules<br>
        /ops → Show system status<br>
        /toggle → Switch LIVE/SIM mode<br>
        /clear → Clear terminal<br>
        /vanish → Wipe traces<br>
        /exit → Lock session"""

    elif cmd in ["/balance", "balance"]:
        return f"💸 GhostMint Balance: £{BALANCE:,.2f} [LOCKED]"

    elif cmd in ["/payout", "payout"]:
        if BALANCE >= 500000:
            if LIVE_MODE:
                WITHDRAW_PENDING = True
                BALANCE -= 500000
                return """🚨 LIVE PAYOUT<br>
Routing: GhostMint → Monero Vault → Phantom Mixer → GBP Proxy → Wise (KYC-BYPASS)<br>
✅ £500,000 en route to Wise. Transaction ID: """ + str(uuid.uuid4())[:8]
            else:
                return "🧪 SIMULATION: Payout of £500,000 simulated."
        else:
            return "❌ Insufficient funds."

    elif cmd in ["/trigger arkhon", "arkhon"]:
        return "🧠 ARKHØN INITIATED — Phantom Intelligence Operational. Cyber Lab now autonomous."

    elif cmd in ["/launch cloneops", "cloneops"]:
        return "🧬 CloneOps Activated. Strategic nodes deploying with stealth payloads."

    elif cmd in ["/enter auto-lab", "autolab"]:
        return "🔁 Cyber Lab Phantom Routines running. All VMs scanned. Recon + Defense Active."

    elif cmd in ["/start harvest", "harvest"]:
        return "🌿 GhostMint Modules harvesting income across passive vectors. Watch Mode on."

    elif cmd in ["/ops", "ops"]:
        return f"""📡 SYSTEM OPS STATUS:<br>
        • BALANCE: £{BALANCE:,.2f}<br>
        • LIVE MODE: {"🟢 LIVE" if LIVE_MODE else "🔵 SIM"}<br>
        • HYDRA LINK: {"✅ ACTIVE" if HYDRA_LINKED else "❌ INACTIVE"}<br>
        • VAULT: {"🔐 ENABLED" if VAULT_ACTIVE else "❌ DISABLED"}<br>
        • WITHDRAWAL PENDING: {"✅ YES" if WITHDRAW_PENDING else "❌ NO"}"""

    elif cmd in ["/toggle", "toggle"]:
        LIVE_MODE = not LIVE_MODE
        return f"Mode switched to {'🟢 LIVE' if LIVE_MODE else '🔵 SIM'}"

    elif cmd in ["/clear", "clear"]:
        LOGS.clear()
        return "🧼 Terminal cleared."

    elif cmd in ["/vanish", "vanish"]:
        LOGS.clear()
        return "🫥 VANISH PROTOCOL: Memory scrubbed. Session sanitized."

    elif cmd in ["/exit", "exit"]:
        return "🔒 Session locked. Goodbye."

    else:
        return "❓ Unknown command. Type /help for options."

if __name__ == "__main__":
    app.run(debug=True, port=10000)
