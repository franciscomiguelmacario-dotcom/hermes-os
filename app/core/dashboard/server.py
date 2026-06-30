from flask import Flask, jsonify

from app.core.startup import Hermes


def create_app():
    hermes = Hermes()
    hermes.kernel.boot()

    app = Flask(__name__)

    @app.route("/")
    def home():
        return """
        <h1>Hermes Dashboard</h1>
        <ul>
            <li><a href="/api/dashboard">Dashboard Data</a></li>
            <li><a href="/api/health">Health</a></li>
            <li><a href="/api/report">Report</a></li>
            <li><a href="/api/tasks">Tasks</a></li>
        </ul>
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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)
