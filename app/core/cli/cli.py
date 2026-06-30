class CLI:

    def __init__(self, brain, logger):
        self.brain = brain
        self.logger = logger

    def run(self):
        self.logger.info("CLI started")

        while True:
            cmd = input("> ").strip()

            if cmd == "exit":
                self.logger.info("CLI stopped")
                return

            if cmd == "help":
                self.logger.info({
                    "commands": [
                        "help",
                        "health",
                        "status",
                        "business",
                        "store",
                        "supplier",
                        "supplier-products",
                        "add-supplier-product <title> | <cost> | <shipping_days> | <url> | <category>",
                        "score-suppliers",
                        "best-supplier-product",
                        "products",
                        "launch-best-product <margin_percent>",
                        "orders",
                        "pending-orders",
                        "order <id>",
                        "create-order <product_id> | <customer_name> | <customer_email> | <quantity>",
                        "fulfill-order <id> | <tracking_number>",
                        "auto-fulfill-orders <tracking_prefix>",
                        "fulfillment-history",
                        "fulfillment-batches",
                        "sales-summary",
                        "best-selling-products",
                        "profit-report",
                        "report",
                        "dashboard",
                        "exit"
                    ]
                })
                continue

            if cmd == "health":
                self.logger.info(self.brain.health_check())
                continue

            if cmd == "status":
                self.logger.info({
                    "agents": {
                        name: getattr(agent, "priority", 1)
                        for name, agent in self.brain.agents.items()
                    }
                })
                continue

            if cmd == "business":
                self.logger.info(self.brain.business_profile())
                continue

            if cmd == "store":
                self.logger.info(self.brain.store_config())
                continue

            if cmd == "supplier":
                self.logger.info(self.brain.supplier_config())
                continue

            if cmd == "supplier-products":
                self.logger.info(self.brain.supplier_products())
                continue

            if cmd.startswith("add-supplier-product "):
                raw = cmd.replace("add-supplier-product ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                title = parts[0]
                cost = parts[1] if len(parts) > 1 else None
                shipping_days = parts[2] if len(parts) > 2 else None
                supplier_url = parts[3] if len(parts) > 3 else None
                category = parts[4] if len(parts) > 4 else None

                self.logger.info(
                    self.brain.add_supplier_product(
                        title,
                        cost,
                        shipping_days,
                        supplier_url,
                        category
                    )
                )
                continue

            if cmd == "score-suppliers":
                self.logger.info(self.brain.score_supplier_products())
                continue

            if cmd == "best-supplier-product":
                self.logger.info(self.brain.best_supplier_product())
                continue

            if cmd.startswith("launch-best-product"):
                parts = cmd.split(" ")
                margin = parts[1] if len(parts) > 1 else None
                self.logger.info(self.brain.launch_best_product(margin))
                continue

            if cmd == "products":
                self.logger.info(self.brain.store_products())
                continue

            if cmd == "orders":
                self.logger.info(self.brain.orders_all())
                continue

            if cmd == "pending-orders":
                self.logger.info(self.brain.pending_orders())
                continue

            if cmd.startswith("order "):
                order_id = cmd.replace("order ", "", 1).strip()
                self.logger.info(self.brain.order_detail(order_id))
                continue

            if cmd.startswith("create-order "):
                raw = cmd.replace("create-order ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                product_id = parts[0]
                customer_name = parts[1] if len(parts) > 1 else None
                customer_email = parts[2] if len(parts) > 2 else None
                quantity = parts[3] if len(parts) > 3 else 1

                self.logger.info(
                    self.brain.create_order(
                        product_id,
                        customer_name,
                        customer_email,
                        quantity
                    )
                )
                continue

            if cmd.startswith("fulfill-order "):
                raw = cmd.replace("fulfill-order ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                order_id = parts[0]
                tracking = parts[1] if len(parts) > 1 else None

                self.logger.info(self.brain.fulfill_order(order_id, tracking))
                continue

            if cmd.startswith("auto-fulfill-orders"):
                parts = cmd.split(" ")
                tracking_prefix = parts[1] if len(parts) > 1 else "HER"

                self.logger.info(
                    self.brain.auto_fulfill_orders(tracking_prefix)
                )
                continue

            if cmd == "fulfillment-history":
                self.logger.info(self.brain.fulfillment_history())
                continue

            if cmd == "fulfillment-batches":
                self.logger.info(self.brain.fulfillment_batches())
                continue

            if cmd == "sales-summary":
                self.logger.info(self.brain.sales_summary())
                continue

            if cmd == "best-selling-products":
                self.logger.info(self.brain.best_selling_products())
                continue

            if cmd == "profit-report":
                self.logger.info(self.brain.profit_report())
                continue

            if cmd == "report":
                self.logger.info(self.brain.report())
                continue

            if cmd == "dashboard":
                self.logger.info(self.brain.dashboard_data())
                continue

            self.logger.info("unknown command")
