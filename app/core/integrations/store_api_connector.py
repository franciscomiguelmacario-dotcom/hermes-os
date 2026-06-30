from datetime import datetime

import requests


class StoreApiConnector:

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
            "auto_sync_on_publish": False,
            "timeout": 20
        }

        saved = self.memory.get("store_api_config", {})

        if not isinstance(saved, dict):
            saved = {}

        config = {**default, **saved}
        self.memory.set("store_api_config", config)

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
        self.memory.set("store_api_config", config)

        return {
            "status": "store_api_config_updated",
            "config": config
        }

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

    def product_payload(self, product):
        description = product.get("description")

        if isinstance(description, dict):
            description_text = self.description_to_text(description)
        else:
            description_text = description or ""

        return {
            "title": product.get("title"),
            "description": description_text,
            "price": product.get("price"),
            "cost": product.get("cost"),
            "sku": f"HERMES-{product.get('id')}",
            "status": "active" if product.get("published") else "draft",
            "category": product.get("category"),
            "seo_title": product.get("seo_title"),
            "seo_description": product.get("seo_description"),
            "source": "hermes",
            "hermes_product_id": product.get("id")
        }

    def description_to_text(self, description):
        lines = []

        if description.get("headline"):
            lines.append(str(description.get("headline")))

        benefits = description.get("benefits", [])

        if benefits:
            lines.append("")
            lines.append("Benefícios:")

            for benefit in benefits:
                lines.append(f"- {benefit}")

        if description.get("cta"):
            lines.append("")
            lines.append(str(description.get("cta")))

        return "\n".join(lines)

    def push_product(self, product):
        config = self.config()
        payload = self.product_payload(product)

        if not config.get("enabled") or config.get("dry_run"):
            result = {
                "status": "dry_run_product_prepared",
                "provider": config.get("provider"),
                "payload": payload,
                "message": "Produto preparado, mas não enviado porque dry_run está ativo."
            }

            self.record_history("push_product", result)
            return result

        provider = config.get("provider")
        base_url = str(config.get("base_url") or "").rstrip("/")

        if not base_url:
            return {
                "status": "error",
                "message": "base_url missing"
            }

        if provider == "shopify":
            endpoint = f"{base_url}/products.json"
            body = {
                "product": {
                    "title": payload["title"],
                    "body_html": payload["description"],
                    "status": payload["status"],
                    "variants": [
                        {
                            "price": payload["price"],
                            "sku": payload["sku"]
                        }
                    ]
                }
            }

        elif provider == "woocommerce":
            endpoint = f"{base_url}/wp-json/wc/v3/products"
            body = {
                "name": payload["title"],
                "type": "simple",
                "regular_price": str(payload["price"]),
                "description": payload["description"],
                "short_description": payload.get("seo_description") or "",
                "sku": payload["sku"],
                "status": "publish" if payload["status"] == "active" else "draft"
            }

        else:
            endpoint = f"{base_url}/products"
            body = payload

        try:
            response = requests.post(
                endpoint,
                json=body,
                headers=self.headers(),
                timeout=int(config.get("timeout") or 20)
            )

            result = {
                "status": "product_pushed",
                "provider": provider,
                "endpoint": endpoint,
                "http_status": response.status_code,
                "response": self.safe_json(response)
            }

            self.record_history("push_product", result)
            return result

        except Exception as error:
            result = {
                "status": "error",
                "message": str(error),
                "provider": provider,
                "endpoint": endpoint
            }

            self.record_history("push_product_error", result)
            return result

    def sync_products(self, products):
        results = []

        for product in products:
            if product.get("published") is True or product.get("status") == "active":
                results.append(self.push_product(product))

        batch = {
            "status": "store_products_synced",
            "created_at": datetime.now().isoformat(),
            "products_checked": len(products),
            "products_synced": len(results),
            "results": results
        }

        self.record_history("sync_products", batch)

        return batch

    def safe_json(self, response):
        try:
            return response.json()
        except Exception:
            return response.text

    def record_history(self, action, result):
        history = self.memory.get("store_api_history", [])

        history.append({
            "created_at": datetime.now().isoformat(),
            "action": action,
            "result": result
        })

        self.memory.set("store_api_history", history)

    def history(self):
        return self.memory.get("store_api_history", [])
