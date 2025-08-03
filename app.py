from flask import Flask, request, jsonify, render_template_string
import time, random

app = Flask(__name__)

# === CORE STATE ===
BALANCE = 6200000.00  # Starting payout balance
LIVE_MODE = True
WITHDRAW_PENDING = False
CLONES_DEPLOYED = 0
AUTO_HARVEST = True
VANISH_TRIGGERED = False
LOGS = []

# === UI (Terminal Style) ===
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>🧬 HYDRA: GHOSTMINT PHANTOM TERMINAL</title>
    <style>
        body { background: #000814; color: #00ffc3; font-family: monospace; padding: 20px; }
        input { background: #000814; color: #00ffc3; border: none; font-size: 1em; width: 100%; }
        .terminal { width: 100%; height: 80vh; overflow-y: auto; border: 1px solid #00ffc3; padding: 10px; }
    </style>
</head>
<body>
    <div class="terminal" id="terminal">
        <p>🔐 HYDRA PHANTOM TERMINAL INITIATED</p>
        <p>LIVE MODE STABLE // ARKHØN CORE ONLINE</p>
        <p>Welcome Operator. Type 'help' to begin.</p>
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
    global BALANCE, LIVE_MODE, LOGS, WITHDRAW_PENDING, VANISH_TRIGGERED, CLONES_DEPLOYED, AUTO_HARVEST

    cmd = request.json.get("cmd", "").lower().strip()
    LOGS.append(cmd)

    if VANISH_TRIGGERED:
        return "🫥 HYDRA VANISHED. No trace remains."

    if cmd == "help":
        return """<b>Available Commands:</b><br>
        - balance → View GhostMint Balance<br>
        - payout → Withdraw £500K to Wise (Live)<br>
        - logs → View full command log<br>
        - clear → Clear terminal logs<br>
        - vanish → Trigger stealth VANISH protocol<br>
        - toggle → Toggle LIVE/SIM mode<br>
        - secure order → Begin dark parts order<br>
        - inject clone → Deploy clone agent<br>
        - arkhön → Activate Cyber Lab PhantomOps<br>
        - status → Full system state<br>
        - exit → Lock session"""

    elif cmd == "balance":
        return f"💸 GhostMint Balance: £{BALANCE:,.2f}"

    elif cmd == "payout":
        if BALANCE >= 500000:
            if LIVE_MODE:
                WITHDRAW_PENDING = True
                BALANCE -= 500000
                return """💸 LIVE PAYOUT: £500,000 INITIATED<br>
                Chain: GhostMint → Monero → Mixer → SideSwitch → Wise<br>
                🔐 Status: Transfer pending to Wise. Awaiting final drop."""
            else:
                return "🧪 SIMULATION: £500K payout simulated."
        else:
            return "❌ Insufficient balance."

    elif cmd == "logs":
        return "<br>".join(LOGS)

    elif cmd == "clear":
        LOGS.clear()
        return "🧼 Terminal cleared."

    elif cmd == "vanish":
        BALANCE = 0
        LOGS.clear()
        WITHDRAW_PENDING = False
        VANISH_TRIGGERED = True
        return "🫥 VANISH PROTOCOL ACTIVATED. Memory wiped. GhostMint cloaked."

    elif cmd == "toggle":
        LIVE_MODE = not LIVE_MODE
        return f"🔁 Mode Toggled: {'🟢 LIVE' if LIVE_MODE else '🔵 SIMULATION'}"

    elif cmd == "secure order":
        if LIVE_MODE and WITHDRAW_PENDING:
            return "🛰️ Secure Order Module Online: Generating invoice to alias drop-point... parts dispatch in progress."
        else:
            return "⚠️ Cannot proceed. Ensure LIVE mode and payout confirmed."

    elif cmd == "inject clone":
        CLONES_DEPLOYED += 1
        return f"👥 Clone Agent #{CLONES_DEPLOYED} injected into recon thread."

    elif cmd == "arkhøn":
        return """🚀 ARKHØN INITIATED<br>
        PhantomOps Active // Cyber Lab Stealth Hooks Armed<br>
        Clone Intelligence Live • Auto-Harvest Running • Secure Payout Path Engaged"""

    elif cmd == "status":
        return f"""
        💠 BALANCE: £{BALANCE:,.2f}<br>
        🔁 MODE: {'LIVE' if LIVE_MODE else 'SIM'}<br>
        🔓 PAYOUT PENDING: {WITHDRAW_PENDING}<br>
        👥 CLONES DEPLOYED: {CLONES_DEPLOYED}<br>
        🔄 AUTO-HARVEST: {'ON' if AUTO_HARVEST else 'OFF'}<br>
        🫥 VANISH: {'TRIGGERED' if VANISH_TRIGGERED else 'ARMED'}"""

    elif cmd == "exit":
        return "🔒 Session locked."

    else:
        return "❓ Unknown command. Type 'help'."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
