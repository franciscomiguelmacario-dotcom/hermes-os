import sys

from app.core.startup import Hermes


def run_cli():
    Hermes().start()


def run_dashboard():
    from app.core.dashboard.server import create_app

    app = create_app()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )


def run_webhooks():
    from app.core.webhooks.order_webhook_server import create_webhook_app

    app = create_webhook_app()
    app.run(
        host="127.0.0.1",
        port=5050,
        debug=False
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        run_dashboard()

    elif len(sys.argv) > 1 and sys.argv[1] in ["webhook", "webhooks"]:
        run_webhooks()

    else:
        run_cli()
