from datetime import datetime


class OrderIntake:

    def __init__(self, order_manager, store, notifications=None, memory=None, logger=None):
        self.order_manager = order_manager
        self.store = store
        self.notifications = notifications
        self.memory = memory
        self.logger = logger

    def normalize(self, payload, provider="custom"):
        if not isinstance(payload, dict):
            return {
                "status": "error",
                "message": "payload must be a dictionary"
            }

        provider = str(provider or payload.get("provider") or "custom").lower()

        if provider == "shopify":
            return self.normalize_shopify(payload)

        if provider == "woocommerce":
            return self.normalize_woocommerce(payload)

        return self.normalize_custom(payload)

    def normalize_custom(self, payload):
        items = payload.get("items", [])

        if not items and payload.get("product_id"):
            items = [
                {
                    "product_id": payload.get("product_id"),
                    "quantity": payload.get("quantity", 1)
                }
            ]

        return {
            "status": "normalized_order",
            "provider": "custom",
            "external_order_id": payload.get("id") or payload.get("order_id"),
            "customer_name": payload.get("customer_name") or payload.get("name"),
            "customer_email": payload.get("customer_email") or payload.get("email"),
            "shipping_address": payload.get("shipping_address") or payload.get("address"),
            "items": items,
            "raw": payload
        }

    def normalize_shopify(self, payload):
        customer = payload.get("customer") or {}
        shipping = payload.get("shipping_address") or {}

        first_name = customer.get("first_name") or shipping.get("first_name") or ""
        last_name = customer.get("last_name") or shipping.get("last_name") or ""
        customer_name = f"{first_name} {last_name}".strip()

        items = []

        for item in payload.get("line_items", []):
            hermes_product_id = self.product_id_from_sku(
                item.get("sku")
            )

            items.append({
                "product_id": hermes_product_id,
                "sku": item.get("sku"),
                "title": item.get("title"),
                "quantity": item.get("quantity", 1),
                "price": item.get("price")
            })

        return {
            "status": "normalized_order",
            "provider": "shopify",
            "external_order_id": payload.get("id") or payload.get("name"),
            "customer_name": customer_name,
            "customer_email": payload.get("email") or customer.get("email"),
            "shipping_address": shipping,
            "items": items,
            "raw": payload
        }

    def normalize_woocommerce(self, payload):
        billing = payload.get("billing") or {}
        shipping = payload.get("shipping") or {}

        first_name = billing.get("first_name") or shipping.get("first_name") or ""
        last_name = billing.get("last_name") or shipping.get("last_name") or ""
        customer_name = f"{first_name} {last_name}".strip()

        items = []

        for item in payload.get("line_items", []):
            hermes_product_id = self.product_id_from_sku(
                item.get("sku")
            )

            items.append({
                "product_id": hermes_product_id,
                "sku": item.get("sku"),
                "title": item.get("name"),
                "quantity": item.get("quantity", 1),
                "price": item.get("price")
            })

        return {
            "status": "normalized_order",
            "provider": "woocommerce",
            "external_order_id": payload.get("id") or payload.get("number"),
            "customer_name": customer_name,
            "customer_email": billing.get("email"),
            "shipping_address": shipping,
            "items": items,
            "raw": payload
        }

    def product_id_from_sku(self, sku):
        if not sku:
            return None

        sku = str(sku)

        if sku.startswith("HERMES-"):
            return sku.replace("HERMES-", "", 1)

        return None

    def find_product(self, item):
        product_id = item.get("product_id")

        if product_id:
            product = self.get_product(product_id)

            if product:
                return product

        sku = item.get("sku")

        if sku:
            product_id = self.product_id_from_sku(sku)

            if product_id:
                product = self.get_product(product_id)

                if product:
                    return product

        title = item.get("title") or item.get("name")

        if title:
            for product in self.store.products():
                if str(product.get("title", "")).lower() == str(title).lower():
                    return product

        return None

    def get_product(self, product_id):
        for product in self.store.products():
            if str(product.get("id")) == str(product_id):
                return product

        return None

    def import_order(self, payload, provider="custom"):
        normalized = self.normalize(payload, provider)

        if normalized.get("status") == "error":
            self.record_history("import_order_error", normalized)
            return normalized

        results = []

        for item in normalized.get("items", []):
            product = self.find_product(item)

            if not product:
                result = {
                    "status": "error",
                    "message": "product not found for order item",
                    "item": item
                }

                results.append(result)
                continue

            created = self.order_manager.create_order(
                product.get("id"),
                normalized.get("customer_name"),
                normalized.get("customer_email"),
                item.get("quantity", 1)
            )

            if created.get("status") == "order_created":
                order = created.get("order", {})

                self.order_manager.update_order(
                    order.get("id"),
                    "external_order_id",
                    normalized.get("external_order_id")
                )

                self.order_manager.update_order(
                    order.get("id"),
                    "order_source",
                    normalized.get("provider")
                )

                self.order_manager.update_order(
                    order.get("id"),
                    "shipping_address",
                    normalized.get("shipping_address")
                )

                self.order_manager.update_order(
                    order.get("id"),
                    "raw_order_payload",
                    normalized.get("raw")
                )

                updated_order = self.order_manager.get_order(order.get("id"))

                if self.notifications:
                    self.notifications.order_confirmation(updated_order)

                created["order"] = updated_order

            results.append(created)

        imported = {
            "status": "order_intake_processed",
            "created_at": datetime.now().isoformat(),
            "provider": normalized.get("provider"),
            "external_order_id": normalized.get("external_order_id"),
            "orders_created": len([
                result for result in results
                if result.get("status") == "order_created"
            ]),
            "results": results,
            "normalized": normalized
        }

        self.record_history("import_order", imported)

        return imported

    def record_history(self, action, result):
        if not self.memory:
            return

        history = self.memory.get("order_intake_history", [])

        history.append({
            "created_at": datetime.now().isoformat(),
            "action": action,
            "result": result
        })

        self.memory.set("order_intake_history", history)

    def history(self):
        if not self.memory:
            return []

        return self.memory.get("order_intake_history", [])
