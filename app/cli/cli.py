import sys

from app.main import main


def run_dashboard():
    from app.core.dashboard.server import create_app

    dashboard = create_app()
    dashboard.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )


def run_webhooks():
    from app.core.webhooks.order_webhook_server import create_webhook_app

    webhook_app = create_webhook_app()
    webhook_app.run(
        host="127.0.0.1",
        port=5050,
        debug=False
    )


def app():
    command = sys.argv[1] if len(sys.argv) > 1 else "start"

    if command in ["start", "run"]:
        main()
        return

    if command == "dashboard":
        run_dashboard()
        return

    if command in ["webhook", "webhooks"]:
        run_webhooks()
        return

    print("usage: hermes [start|dashboard|webhooks]")
