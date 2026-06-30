from datetime import datetime

import requests


class SupplierApiConnector:

    def __init__(self, memory, logger=None):
        self.memory = memory
        self.logger = logger

    def config(self):
        default = {
            "enabled": False,
            "provider": "dry_run",
            "base_url": "",
            "api_key": "",
            "api_secret": "",
            "access_token": "",
            "dry_run": True,
            "timeout": 20
        }

        saved = self.memory.get("supplier_api_config", {})

        if not isinstance(saved, dict):
            saved = {}

        config = {**default, **saved}
        self.memory.set("supplier_api_config", config)

        return config

    def set_config_value(self, key, value):
        config = self.config()

        if key not in config:
            return {
                "status": "error",
                "message": "invalid config key",
                "valid_keys": list(config.keys())
            }

        if str(value).lower() in ["true", "yes", "1"]:
            value = True
        elif str(value).lower() in ["false", "no", "0"]:
            value = False
        else:
            try:
                if "." in str(value):
                    value = float(value)
                else:
                    value = int(value)
            except Exception:
                pass

        config[key] = value
        self.memory.set("supplier_api_config", config)

        return {
            "status": "supplier_api_config_updated",
            "config": self.safe_config(config)
        }

    def safe_config(self, config):
        safe = dict(config)

        for key in ["api_key", "api_secret", "access_token"]:
            if safe.get(key):
                safe[key] = "***configured***"

        return safe

    def headers(self):
        config = self.config()

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Hermes-OS/0.1"
        }

        token = config.get("access_token")

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def build_order_payload(self, order):
        return {
            "order_id": order.get("id"),
            "product_id": order.get("product_id"),
            "product_title": order.get("product_title"),
            "quantity": order.get("quantity"),
            "customer_name": order.get("customer_name"),
            "customer_email": order.get("customer_email"),
            "supplier_url": order.get("supplier_url"),
            "shipping_address": order.get("shipping_address"),
            "source": "hermes"
        }

    def submit_order(self, order):
        config = self.config()
        payload = self.build_order_payload(order)

        if not config.get("enabled") or config.get("dry_run"):
            result = {
                "status": "dry_run_supplier_order_prepared",
                "provider": config.get("provider"),
                "payload": payload,
                "message": "Encomenda preparada para fornecedor, mas não enviada porque dry_run está ativo."
            }

            self.record_history("submit_order", result)
            return result

        base_url = str(config.get("base_url") or "").rstrip("/")

        if not base_url:
            return {
                "status": "error",
                "message": "base_url missing"
            }

        endpoint = f"{base_url}/orders"

        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers(),
                timeout=int(config.get("timeout") or 20)
            )

            result = {
                "status": "supplier_order_submitted",
                "provider": config.get("provider"),
                "endpoint": endpoint,
                "http_status": response.status_code,
                "response": self.safe_json(response),
                "payload": payload
            }

            self.record_history("submit_order", result)
            return result

        except Exception as error:
            result = {
                "status": "error",
                "message": str(error),
                "provider": config.get("provider"),
                "endpoint": endpoint,
                "payload": payload
            }

            self.record_history("submit_order_error", result)
            return result

    def submit_orders(self, orders):
        results = []

        for order in orders:
            if order.get("fulfillment_status") == "pending":
                results.append(self.submit_order(order))

        batch = {
            "status": "supplier_orders_processed",
            "created_at": datetime.now().isoformat(),
            "orders_checked": len(orders),
            "orders_sent": len(results),
            "results": results
        }

        self.record_history("submit_orders", batch)

        return batch

    def safe_json(self, response):
        try:
            return response.json()
        except Exception:
            return response.text

    def record_history(self, action, result):
        history = self.memory.get("supplier_api_history", [])

        history.append({
            "created_at": datetime.now().isoformat(),
            "action": action,
            "result": result
        })

        self.memory.set("supplier_api_history", history)

    def history(self):
        return self.memory.get("supplier_api_history", [])
