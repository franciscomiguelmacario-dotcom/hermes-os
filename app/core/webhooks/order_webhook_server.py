import os
import threading
import time

from flask import Flask, jsonify, request

from app.core.startup import Hermes


def create_webhook_app():
    app = Flask(__name__)

    hermes = Hermes()
    hermes.kernel.boot()

    running = {"enabled": True}

    def background_loop():
        while running["enabled"]:
            try:
                hermes.kernel.run_tick()
            except Exception as error:
                hermes.logger.info(f"Webhook runtime error: {error}")

            time.sleep(1)

    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()

    app.config["HERMES"] = hermes
    app.config["RUNNING"] = running

    def brain():
        return app.config["HERMES"].brain

    def webhook_secret():
        return os.getenv("HERMES_WEBHOOK_SECRET", "").strip()

    def authorized():
        secret = webhook_secret()

        if not secret:
            return True

        received = (
            request.headers.get("X-Hermes-Token")
            or request.args.get("token")
            or ""
        ).strip()

        return received == secret

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "status": "hermes_webhook_server_ready",
            "endpoints": {
                "health": "/health",
                "custom_order": "/webhook/orders/custom",
                "shopify_order": "/webhook/orders/shopify",
                "woocommerce_order": "/webhook/orders/woocommerce",
                "order_intake_history": "/webhook/order-intake/history"
            },
            "security": {
                "secret_required": bool(webhook_secret()),
                "header": "X-Hermes-Token"
            }
        })

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "service": "hermes_order_webhooks"
        })

    @app.route("/webhook/orders/<provider>", methods=["POST"])
    def receive_order(provider):
        if not authorized():
            return jsonify({
                "status": "error",
                "message": "unauthorized"
            }), 401

        try:
            payload = request.get_json(force=True, silent=False)
        except Exception as error:
            return jsonify({
                "status": "error",
                "message": "invalid json",
                "error": str(error)
            }), 400

        result = brain().import_order(payload, provider)

        http_status = 200

        if result.get("status") == "error":
            http_status = 400

        return jsonify(result), http_status

    @app.route("/webhook/order-intake/history", methods=["GET"])
    def order_intake_history():
        if not authorized():
            return jsonify({
                "status": "error",
                "message": "unauthorized"
            }), 401

        return jsonify({
            "status": "ok",
            "history": brain().order_intake_history()
        })

    @app.route("/webhook/orders/test", methods=["POST", "GET"])
    def test_order():
        if not authorized():
            return jsonify({
                "status": "error",
                "message": "unauthorized"
            }), 401

        payload = {
            "id": "WEBHOOK-TEST-1001",
            "product_id": 1,
            "quantity": 1,
            "customer_name": "Cliente Webhook",
            "customer_email": "webhook@email.com",
            "shipping_address": {
                "address1": "Rua Webhook 1",
                "city": "Lisboa",
                "country": "Portugal",
                "postal_code": "1000-000"
            }
        }

        result = brain().import_order(payload, "custom")

        return jsonify(result)

    return app


def run_webhook_server():
    app = create_webhook_app()
    app.run(
        host="127.0.0.1",
        port=5050,
        debug=False
    )


if __name__ == "__main__":
    run_webhook_server()
