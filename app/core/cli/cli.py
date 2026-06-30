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
                        "store-api",
                        "set-store-api <key> <value>",
                        "push-product-store <product_id>",
                        "sync-store-products",
                        "store-api-history",
                        "supplier",
                        "supplier-api",
                        "set-supplier-api <key> <value>",
                        "submit-order-supplier <order_id>",
                        "submit-pending-orders-supplier",
                        "mark-supplier-tracking <order_id> | <tracking_number>",
                        "fulfillment-pipeline-history",
                        "supplier-api-history",
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
                        "notifications",
                        "pending-notifications",
                        "send-notifications",
                        "notification-batches",
                        "support-tickets",
                        "pending-support",
                        "support-ticket <id>",
                        "create-support-ticket <email> | <subject> | <message> | <order_id>",
                        "reply-support-ticket <id> | <message>",
                        "close-support-ticket <id>",
                        "auto-reply-support <id>",
                        "auto-reply-support-all",
                        "support-batches",
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

            if cmd == "store-api":
                self.logger.info(self.brain.store_api_config())
                continue

            if cmd.startswith("set-store-api "):
                parts = cmd.split(" ", 2)

                if len(parts) < 3:
                    self.logger.info("usage: set-store-api <key> <value>")
                    continue

                _, key, value = parts

                self.logger.info(
                    self.brain.set_store_api_config(key, value)
                )
                continue

            if cmd.startswith("push-product-store "):
                product_id = cmd.replace("push-product-store ", "", 1).strip()
                self.logger.info(self.brain.push_product_to_store(product_id))
                continue

            if cmd == "sync-store-products":
                self.logger.info(self.brain.sync_products_to_store())
                continue

            if cmd == "store-api-history":
                self.logger.info(self.brain.store_api_history())
                continue

            if cmd == "supplier":
                self.logger.info(self.brain.supplier_config())
                continue

            if cmd == "supplier-api":
                self.logger.info(self.brain.supplier_api_config())
                continue

            if cmd.startswith("set-supplier-api "):
                parts = cmd.split(" ", 2)

                if len(parts) < 3:
                    self.logger.info("usage: set-supplier-api <key> <value>")
                    continue

                _, key, value = parts

                self.logger.info(
                    self.brain.set_supplier_api_config(key, value)
                )
                continue

            if cmd.startswith("submit-order-supplier "):
                order_id = cmd.replace("submit-order-supplier ", "", 1).strip()
                self.logger.info(self.brain.submit_order_to_supplier(order_id))
                continue

            if cmd == "submit-pending-orders-supplier":
                self.logger.info(self.brain.submit_pending_orders_to_supplier())
                continue

            if cmd.startswith("mark-supplier-tracking "):
                raw = cmd.replace("mark-supplier-tracking ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                order_id = parts[0]
                tracking = parts[1] if len(parts) > 1 else None

                self.logger.info(
                    self.brain.mark_supplier_tracking(order_id, tracking)
                )
                continue

            if cmd == "fulfillment-pipeline-history":
                self.logger.info(self.brain.fulfillment_pipeline_history())
                continue

            if cmd == "supplier-api-history":
                self.logger.info(self.brain.supplier_api_history())
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

            if cmd == "notifications":
                self.logger.info(self.brain.notifications_all())
                continue

            if cmd == "pending-notifications":
                self.logger.info(self.brain.pending_notifications())
                continue

            if cmd == "send-notifications":
                self.logger.info(self.brain.send_notifications())
                continue

            if cmd == "notification-batches":
                self.logger.info(self.brain.notification_batches())
                continue

            if cmd == "support-tickets":
                self.logger.info(self.brain.support_tickets())
                continue

            if cmd == "pending-support":
                self.logger.info(self.brain.pending_support_tickets())
                continue

            if cmd.startswith("support-ticket "):
                ticket_id = cmd.replace("support-ticket ", "", 1).strip()
                self.logger.info(self.brain.support_ticket_detail(ticket_id))
                continue

            if cmd.startswith("create-support-ticket "):
                raw = cmd.replace("create-support-ticket ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                email = parts[0] if len(parts) > 0 else None
                subject = parts[1] if len(parts) > 1 else None
                message = parts[2] if len(parts) > 2 else None
                order_id = parts[3] if len(parts) > 3 else None

                self.logger.info(
                    self.brain.create_support_ticket(
                        email,
                        subject,
                        message,
                        order_id
                    )
                )
                continue

            if cmd.startswith("reply-support-ticket "):
                raw = cmd.replace("reply-support-ticket ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                ticket_id = parts[0]
                message = parts[1] if len(parts) > 1 else ""

                self.logger.info(
                    self.brain.reply_support_ticket(ticket_id, message)
                )
                continue

            if cmd.startswith("close-support-ticket "):
                ticket_id = cmd.replace("close-support-ticket ", "", 1).strip()
                self.logger.info(self.brain.close_support_ticket(ticket_id))
                continue

            if cmd.startswith("auto-reply-support "):
                ticket_id = cmd.replace("auto-reply-support ", "", 1).strip()
                self.logger.info(self.brain.auto_reply_support_ticket(ticket_id))
                continue

            if cmd == "auto-reply-support-all":
                self.logger.info(self.brain.auto_reply_support_all())
                continue

            if cmd == "support-batches":
                self.logger.info(self.brain.support_batches())
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

            if cmd == "store-autopilot-history":
                self.logger.info(self.brain.store_autopilot_history())
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

            if cmd == "report":
                self.logger.info(self.brain.report())
                continue

            if cmd == "dashboard":
                self.logger.info(self.brain.dashboard_data())
                continue

            self.logger.info("unknown command")
