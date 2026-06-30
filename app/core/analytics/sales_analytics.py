class SalesAnalytics:

    def __init__(self, order_manager, memory, logger=None):
        self.order_manager = order_manager
        self.memory = memory
        self.logger = logger

    def summary(self):
        orders = self.order_manager.all()

        total_orders = len(orders)
        pending_orders = len([
            order for order in orders
            if order.get("fulfillment_status") == "pending"
        ])
        fulfilled_orders = len([
            order for order in orders
            if order.get("fulfillment_status") == "fulfilled"
        ])

        revenue = sum(float(order.get("total") or 0) for order in orders)
        costs = sum(float(order.get("total_cost") or 0) for order in orders)
        profit = sum(float(order.get("estimated_profit") or 0) for order in orders)

        average_order_value = 0
        if total_orders > 0:
            average_order_value = revenue / total_orders

        result = {
            "status": "sales_summary",
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "fulfilled_orders": fulfilled_orders,
            "revenue": round(revenue, 2),
            "costs": round(costs, 2),
            "profit": round(profit, 2),
            "average_order_value": round(average_order_value, 2)
        }

        self.memory.set("last_sales_summary", result)

        return result

    def best_selling_products(self):
        orders = self.order_manager.all()
        products = {}

        for order in orders:
            product_id = order.get("product_id")
            title = order.get("product_title")
            quantity = int(order.get("quantity") or 0)
            revenue = float(order.get("total") or 0)
            profit = float(order.get("estimated_profit") or 0)

            if product_id not in products:
                products[product_id] = {
                    "product_id": product_id,
                    "title": title,
                    "quantity_sold": 0,
                    "revenue": 0,
                    "profit": 0
                }

            products[product_id]["quantity_sold"] += quantity
            products[product_id]["revenue"] += revenue
            products[product_id]["profit"] += profit

        ranked = sorted(
            products.values(),
            key=lambda item: item["quantity_sold"],
            reverse=True
        )

        for product in ranked:
            product["revenue"] = round(product["revenue"], 2)
            product["profit"] = round(product["profit"], 2)

        self.memory.set("best_selling_products", ranked)

        return {
            "status": "best_selling_products",
            "products": ranked
        }

    def profit_report(self):
        summary = self.summary()
        best_products = self.best_selling_products()

        report = {
            "status": "profit_report",
            "summary": summary,
            "best_selling_products": best_products.get("products", [])
        }

        self.memory.set("last_profit_report", report)

        return report
