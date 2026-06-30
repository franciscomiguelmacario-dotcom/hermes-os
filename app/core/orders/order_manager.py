from datetime import datetime


class OrderManager:

    def __init__(self, store, memory, logger=None):
        self.store = store
        self.memory = memory
        self.logger = logger

    def all(self):
        return self.memory.get("orders", [])

    def pending(self):
        return [
            order for order in self.all()
            if order.get("fulfillment_status") == "pending"
        ]

    def get_order(self, order_id):
        for order in self.all():
            if order["id"] == int(order_id):
                return order

        return None

    def get_product(self, product_id):
        for product in self.store.products():
            if product["id"] == int(product_id):
                return product

        return None

    def create_order(
        self,
        product_id,
        customer_name=None,
        customer_email=None,
        quantity=1
    ):
        product = self.get_product(product_id)

        if not product:
            return {
                "status": "error",
                "message": "product not found"
            }

        quantity = int(quantity or 1)
        price = float(product.get("price") or 0)
        cost = float(product.get("cost") or 0)

        total = price * quantity
        total_cost = cost * quantity
        estimated_profit = total - total_cost

        orders = self.all()

        order = {
            "id": len(orders) + 1,
            "created_at": datetime.now().isoformat(),
            "product_id": product["id"],
            "product_title": product.get("title"),
            "customer_name": customer_name,
            "customer_email": customer_email,
            "quantity": quantity,
            "price": price,
            "cost": cost,
            "total": round(total, 2),
            "total_cost": round(total_cost, 2),
            "estimated_profit": round(estimated_profit, 2),
            "payment_status": "paid",
            "fulfillment_status": "pending",
            "tracking_number": None,
            "supplier_url": product.get("supplier_url"),
            "status": "new"
        }

        orders.append(order)
        self.memory.set("orders", orders)

        return {
            "status": "order_created",
            "order": order
        }

    def update_order(self, order_id, key, value):
        orders = self.all()

        for order in orders:
            if order["id"] == int(order_id):
                order[key] = value
                self.memory.set("orders", orders)

                return {
                    "status": "order_updated",
                    "order": order
                }

        return {
            "status": "error",
            "message": "order not found"
        }

    def fulfill_order(self, order_id, tracking_number=None):
        orders = self.all()

        for order in orders:
            if order["id"] == int(order_id):
                order["fulfillment_status"] = "fulfilled"
                order["status"] = "fulfilled"
                order["tracking_number"] = tracking_number
                order["fulfilled_at"] = datetime.now().isoformat()

                self.memory.set("orders", orders)

                history = self.memory.get("fulfillment_history", [])
                history.append(order)
                self.memory.set("fulfillment_history", history)

                return {
                    "status": "order_fulfilled",
                    "order": order
                }

        return {
            "status": "error",
            "message": "order not found"
        }

    def auto_fulfill_pending(self, tracking_prefix="HER"):
        pending_orders = self.pending()
        results = []

        for order in pending_orders:
            if not order.get("supplier_url"):
                result = self.update_order(
                    order["id"],
                    "status",
                    "manual_review"
                )

                results.append({
                    "status": "manual_review_required",
                    "reason": "missing supplier_url",
                    "order": result.get("order")
                })

                continue

            tracking_number = f"{tracking_prefix}{int(order['id']):06d}"

            results.append(
                self.fulfill_order(
                    order["id"],
                    tracking_number
                )
            )

        batch = {
            "created_at": datetime.now().isoformat(),
            "orders_processed": len(results),
            "results": results
        }

        batches = self.memory.get("fulfillment_batches", [])
        batches.append(batch)
        self.memory.set("fulfillment_batches", batches)

        return {
            "status": "auto_fulfillment_finished",
            "orders_processed": len(results),
            "batch": batch
        }

    def fulfillment_history(self):
        return self.memory.get("fulfillment_history", [])

    def fulfillment_batches(self):
        return self.memory.get("fulfillment_batches", [])
