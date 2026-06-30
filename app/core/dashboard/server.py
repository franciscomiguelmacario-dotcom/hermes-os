from flask import Flask, jsonify

from app.core.startup import Hermes


def create_app():
    hermes = Hermes()
    hermes.kernel.boot()

    app = Flask(__name__)

    @app.route("/")
    def home():
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Hermes Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111;
            color: #eee;
            padding: 30px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin-top: 25px;
        }

        .card {
            background: #1d1d1d;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 18px;
        }

        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background: #000;
            padding: 12px;
            border-radius: 8px;
            max-height: 400px;
            overflow: auto;
        }

        button {
            padding: 10px 14px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            margin: 4px;
        }
    </style>
</head>
<body>
    <h1>Hermes Dashboard</h1>
    <p>Business automation control panel</p>

    <button onclick="loadDashboard()">Refresh</button>
    <button onclick="runAction('/api/action/autopilot')">Autopilot</button>
    <button onclick="runAction('/api/action/business-cycle')">Business Cycle</button>
    <button onclick="runAction('/api/action/export-obsidian')">Export Obsidian</button>
    <button onclick="runAction('/api/action/backup')">Backup</button>
    <button onclick="runAction('/api/action/clear-tasks')">Clear Tasks</button>

    <div class="grid">
        <div class="card">
            <h2>Health</h2>
            <pre id="health">Loading...</pre>
        </div>

        <div class="card">
            <h2>Business Profile</h2>
            <pre id="business">Loading...</pre>
        </div>

        <div class="card">
            <h2>Next Action</h2>
            <pre id="next">Loading...</pre>
        </div>

        <div class="card">
            <h2>Tasks</h2>
            <pre id="tasks">Loading...</pre>
        </div>

        <div class="card">
            <h2>Agents</h2>
            <pre id="agents">Loading...</pre>
        </div>

        <div class="card">
            <h2>Cycle History</h2>
            <pre id="cycles">Loading...</pre>
        </div>

        <div class="card">
            <h2>Last Action Result</h2>
            <pre id="result">None</pre>
        </div>
    </div>

    <script>
        async function loadDashboard() {
            const response = await fetch("/api/dashboard");
            const data = await response.json();

            document.getElementById("health").textContent = JSON.stringify(data.health, null, 2);
            document.getElementById("business").textContent = JSON.stringify(data.business_profile, null, 2);
            document.getElementById("next").textContent = JSON.stringify(data.next_action, null, 2);
            document.getElementById("tasks").textContent = JSON.stringify(data.tasks, null, 2);
            document.getElementById("agents").textContent = JSON.stringify(data.agents, null, 2);
            document.getElementById("cycles").textContent = JSON.stringify(data.cycle_history, null, 2);
        }

        async function runAction(url) {
            document.getElementById("result").textContent = "Running...";

            const response = await fetch(url, { method: "POST" });
            const data = await response.json();

            document.getElementById("result").textContent = JSON.stringify(data, null, 2);

            await loadDashboard();
        }

        loadDashboard();
    </script>
</body>
</html>
        """

    @app.route("/api/dashboard")
    def dashboard():
        return jsonify(hermes.brain.dashboard_data())

    @app.route("/api/health")
    def health():
        return jsonify(hermes.brain.health_check())

    @app.route("/api/report")
    def report():
        return jsonify(hermes.brain.report())

    @app.route("/api/tasks")
    def tasks():
        return jsonify(hermes.brain.tasks.all())

    @app.route("/api/action/autopilot", methods=["POST"])
    def action_autopilot():
        return jsonify(hermes.brain.autopilot_once())

    @app.route("/api/action/business-cycle", methods=["POST"])
    def action_business_cycle():
        return jsonify(hermes.brain.run_business_cycle())

    @app.route("/api/action/export-obsidian", methods=["POST"])
    def action_export_obsidian():
        return jsonify(hermes.brain.export_obsidian_report())

    @app.route("/api/action/backup", methods=["POST"])
    def action_backup():
        return jsonify(hermes.brain.create_backup())

    @app.route("/api/action/clear-tasks", methods=["POST"])
    def action_clear_tasks():
        return jsonify(hermes.brain.clear_tasks())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)
