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
                        "campaigns",
                        "create-campaign <product_id> | <budget> | <channel>",
                        "create-best-campaign <budget> | <channel>",
                        "launch-campaign <id>",
                        "pause-campaign <id>",
                        "update-campaign-metrics <id> | <impressions> | <clicks> | <orders> | <revenue> | <profit> | <spend>",
                        "simulate-campaign <id>",
                        "optimize-campaigns",
                        "campaign-performance",
                        "campaign-report",
                        "store-autopilot-config",
                        "set-store-autopilot <key> <value>",
                        "store-autopilot-safety <budget>",
                        "store-autopilot <margin> | <budget> | <channel> | <tracking_prefix>",
                        "store-autopilot-history",
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

            if cmd == "campaigns":
                self.logger.info(self.brain.campaigns_all())
                continue

            if cmd.startswith("create-campaign "):
                raw = cmd.replace("create-campaign ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                product_id = parts[0]
                budget = parts[1] if len(parts) > 1 else 10
                channel = parts[2] if len(parts) > 2 else "facebook_ads"

                self.logger.info(
                    self.brain.create_campaign(
                        product_id,
                        budget,
                        channel
                    )
                )
                continue

            if cmd.startswith("create-best-campaign"):
                raw = cmd.replace("create-best-campaign", "", 1).strip()
                parts = [p.strip() for p in raw.split("|") if p.strip()]

                budget = parts[0] if len(parts) > 0 else 10
                channel = parts[1] if len(parts) > 1 else "facebook_ads"

                self.logger.info(
                    self.brain.create_best_campaign(
                        budget,
                        channel
                    )
                )
                continue

            if cmd.startswith("launch-campaign "):
                campaign_id = cmd.replace("launch-campaign ", "", 1).strip()
                self.logger.info(self.brain.launch_campaign(campaign_id))
                continue

            if cmd.startswith("pause-campaign "):
                campaign_id = cmd.replace("pause-campaign ", "", 1).strip()
                self.logger.info(self.brain.pause_campaign(campaign_id))
                continue

            if cmd.startswith("update-campaign-metrics "):
                raw = cmd.replace("update-campaign-metrics ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                campaign_id = parts[0]
                impressions = parts[1] if len(parts) > 1 else 0
                clicks = parts[2] if len(parts) > 2 else 0
                orders = parts[3] if len(parts) > 3 else 0
                revenue = parts[4] if len(parts) > 4 else 0
                profit = parts[5] if len(parts) > 5 else 0
                spend = parts[6] if len(parts) > 6 else 0

                self.logger.info(
                    self.brain.update_campaign_metrics(
                        campaign_id,
                        impressions,
                        clicks,
                        orders,
                        revenue,
                        profit,
                        spend
                    )
                )
                continue

            if cmd.startswith("simulate-campaign "):
                campaign_id = cmd.replace("simulate-campaign ", "", 1).strip()
                self.logger.info(self.brain.simulate_campaign(campaign_id))
                continue

            if cmd == "optimize-campaigns":
                self.logger.info(self.brain.optimize_campaigns())
                continue

            if cmd == "campaign-performance":
                self.logger.info(self.brain.campaign_performance())
                continue

            if cmd == "campaign-report":
                self.logger.info(self.brain.campaign_report())
                continue

            if cmd == "store-autopilot-config":
                self.logger.info(self.brain.store_autopilot_config())
                continue

            if cmd.startswith("set-store-autopilot "):
                parts = cmd.split(" ", 2)

                if len(parts) < 3:
                    self.logger.info("usage: set-store-autopilot <key> <value>")
                    continue

                _, key, value = parts

                self.logger.info(
                    self.brain.set_store_autopilot_config(key, value)
                )
                continue

            if cmd.startswith("store-autopilot-safety"):
                parts = cmd.split(" ")
                budget = parts[1] if len(parts) > 1 else 0

                self.logger.info(
                    self.brain.store_autopilot_safety(budget)
                )
                continue

            if cmd.startswith("store-autopilot"):
                raw = cmd.replace("store-autopilot", "", 1).strip()
                parts = [p.strip() for p in raw.split("|") if p.strip()]

                margin = parts[0] if len(parts) > 0 else 40
                budget = parts[1] if len(parts) > 1 else 10
                channel = parts[2] if len(parts) > 2 else "facebook_ads"
                tracking_prefix = parts[3] if len(parts) > 3 else "HER"

                self.logger.info(
                    self.brain.run_store_autopilot(
                        margin,
                        budget,
                        channel,
                        tracking_prefix
                    )
                )
                continue

            if cmd == "store-autopilot-history":
                self.logger.info(self.brain.store_autopilot_history())
                continue

            if cmd == "report":
                self.logger.info(self.brain.report())
                continue

            if cmd == "dashboard":
                self.logger.info(self.brain.dashboard_data())
                continue

            self.logger.info("unknown command")
