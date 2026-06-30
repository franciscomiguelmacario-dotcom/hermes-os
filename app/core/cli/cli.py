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
                        "set-business <key> <value>",
                        "store",
                        "set-store <key> <value>",
                        "supplier",
                        "set-supplier <key> <value>",
                        "supplier-products",
                        "add-supplier-product <title> | <cost> | <shipping_days> | <url> | <category>",
                        "search-supplier <keyword>",
                        "score-suppliers",
                        "best-supplier-product",
                        "pricing",
                        "price <cost> <shipping> <margin_percent>",
                        "products",
                        "product <id>",
                        "create-product <title> | <price> | <cost>",
                        "update-product <id> <key> <value>",
                        "delete-product <id>",
                        "import-product <supplier_product_id> <margin_percent>",
                        "import-product-search <keyword> | <margin_percent>",
                        "import-history",
                        "publish-product <id>",
                        "unpublish-product <id>",
                        "publish-history",
                        "launch-product <supplier_product_id> <margin_percent>",
                        "launch-product-search <keyword> | <margin_percent>",
                        "launch-best-product <margin_percent>",
                        "launch-history",
                        "orders",
                        "pending-orders",
                        "order <id>",
                        "create-order <product_id> | <customer_name> | <customer_email> | <quantity>",
                        "update-order <id> <key> <value>",
                        "fulfill-order <id> | <tracking_number>",
                        "fulfillment-history",
                        "tasks",
                        "clear-tasks",
                        "task <texto>",
                        "workflows",
                        "workflow dropshipping",
                        "next-action",
                        "autopilot",
                        "autopilot-cycle <steps>",
                        "business-cycle",
                        "cycle-history",
                        "dashboard",
                        "report",
                        "export-report",
                        "export-report-md",
                        "export-obsidian",
                        "backup",
                        "backups",
                        "snapshot",
                        "snapshots",
                        "memory",
                        "memory-key <key>",
                        "chat <texto>",
                        "jarvis <texto>",
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

            if cmd.startswith("set-business "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    self.logger.info("usage: set-business <key> <value>")
                    continue
                _, key, value = parts
                self.logger.info(self.brain.set_business_value(key, value))
                continue

            if cmd == "store":
                self.logger.info(self.brain.store_config())
                continue

            if cmd.startswith("set-store "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    self.logger.info("usage: set-store <key> <value>")
                    continue
                _, key, value = parts
                self.logger.info(self.brain.set_store_value(key, value))
                continue

            if cmd == "supplier":
                self.logger.info(self.brain.supplier_config())
                continue

            if cmd.startswith("set-supplier "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    self.logger.info("usage: set-supplier <key> <value>")
                    continue
                _, key, value = parts
                self.logger.info(self.brain.set_supplier_value(key, value))
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

            if cmd.startswith("search-supplier "):
                keyword = cmd.replace("search-supplier ", "", 1).strip()
                self.logger.info(self.brain.search_supplier_products(keyword))
                continue

            if cmd == "score-suppliers":
                self.logger.info(self.brain.score_supplier_products())
                continue

            if cmd == "best-supplier-product":
                self.logger.info(self.brain.best_supplier_product())
                continue

            if cmd == "pricing":
                self.logger.info(self.brain.pricing_config())
                continue

            if cmd.startswith("price "):
                parts = cmd.split(" ")
                cost = parts[1] if len(parts) > 1 else 0
                shipping = parts[2] if len(parts) > 2 else 0
                margin = parts[3] if len(parts) > 3 else None
                self.logger.info(self.brain.calculate_price(cost, shipping, margin))
                continue

            if cmd == "products":
                self.logger.info(self.brain.store_products())
                continue

            if cmd.startswith("product "):
                product_id = cmd.replace("product ", "", 1).strip()
                self.logger.info(self.brain.product_detail(product_id))
                continue

            if cmd.startswith("create-product "):
                raw = cmd.replace("create-product ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                title = parts[0]
                price = parts[1] if len(parts) > 1 else None
                cost = parts[2] if len(parts) > 2 else None

                self.logger.info(self.brain.create_store_product(title, price, cost))
                continue

            if cmd.startswith("update-product "):
                parts = cmd.split(" ", 3)
                if len(parts) < 4:
                    self.logger.info("usage: update-product <id> <key> <value>")
                    continue
                _, product_id, key, value = parts
                self.logger.info(self.brain.update_store_product(product_id, key, value))
                continue

            if cmd.startswith("delete-product "):
                product_id = cmd.replace("delete-product ", "", 1).strip()
                self.logger.info(self.brain.delete_store_product(product_id))
                continue

            if cmd.startswith("import-product-search "):
                raw = cmd.replace("import-product-search ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                keyword = parts[0]
                margin = parts[1] if len(parts) > 1 else None

                self.logger.info(self.brain.import_supplier_search(keyword, margin))
                continue

            if cmd.startswith("import-product "):
                parts = cmd.split(" ")

                supplier_product_id = parts[1] if len(parts) > 1 else None
                margin = parts[2] if len(parts) > 2 else None

                if not supplier_product_id:
                    self.logger.info("usage: import-product <supplier_product_id> <margin_percent>")
                    continue

                self.logger.info(self.brain.import_supplier_product(supplier_product_id, margin))
                continue

            if cmd == "import-history":
                self.logger.info(self.brain.product_import_history())
                continue

            if cmd.startswith("publish-product "):
                product_id = cmd.replace("publish-product ", "", 1).strip()
                self.logger.info(self.brain.publish_product(product_id))
                continue

            if cmd.startswith("unpublish-product "):
                product_id = cmd.replace("unpublish-product ", "", 1).strip()
                self.logger.info(self.brain.unpublish_product(product_id))
                continue

            if cmd == "publish-history":
                self.logger.info(self.brain.product_publish_history())
                continue

            if cmd.startswith("launch-best-product"):
                parts = cmd.split(" ")
                margin = parts[1] if len(parts) > 1 else None
                self.logger.info(self.brain.launch_best_product(margin))
                continue

            if cmd.startswith("launch-product-search "):
                raw = cmd.replace("launch-product-search ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                keyword = parts[0]
                margin = parts[1] if len(parts) > 1 else None

                self.logger.info(self.brain.launch_product_search(keyword, margin))
                continue

            if cmd.startswith("launch-product "):
                parts = cmd.split(" ")

                supplier_product_id = parts[1] if len(parts) > 1 else None
                margin = parts[2] if len(parts) > 2 else None

                if not supplier_product_id:
                    self.logger.info("usage: launch-product <supplier_product_id> <margin_percent>")
                    continue

                self.logger.info(self.brain.launch_product(supplier_product_id, margin))
                continue

            if cmd == "launch-history":
                self.logger.info(self.brain.product_launch_history())
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

            if cmd.startswith("update-order "):
                parts = cmd.split(" ", 3)

                if len(parts) < 4:
                    self.logger.info("usage: update-order <id> <key> <value>")
                    continue

                _, order_id, key, value = parts
                self.logger.info(self.brain.update_order(order_id, key, value))
                continue

            if cmd.startswith("fulfill-order "):
                raw = cmd.replace("fulfill-order ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                order_id = parts[0]
                tracking = parts[1] if len(parts) > 1 else None

                self.logger.info(self.brain.fulfill_order(order_id, tracking))
                continue

            if cmd == "fulfillment-history":
                self.logger.info(self.brain.fulfillment_history())
                continue

            if cmd == "tasks":
                self.logger.info(self.brain.tasks.all())
                continue

            if cmd == "clear-tasks":
                self.logger.info(self.brain.clear_tasks())
                continue

            if cmd.startswith("task "):
                title = cmd[5:]
                self.logger.info(self.brain.create_task(title))
                continue

            if cmd == "workflows":
                self.logger.info(self.brain.workflows.list())
                continue

            if cmd.startswith("workflow "):
                name = cmd[9:]
                self.logger.info(self.brain.run_workflow(name))
                continue

            if cmd == "next-action":
                self.logger.info(self.brain.next_action())
                continue

            if cmd == "autopilot":
                self.logger.info(self.brain.autopilot_once())
                continue

            if cmd.startswith("autopilot-cycle"):
                parts = cmd.split(" ")
                max_steps = 5

                if len(parts) == 2:
                    max_steps = int(parts[1])

                self.logger.info(self.brain.autopilot_cycle(max_steps))
                continue

            if cmd == "business-cycle":
                self.logger.info(self.brain.run_business_cycle())
                continue

            if cmd == "cycle-history":
                self.logger.info(self.brain.business_cycle_history())
                continue

            if cmd == "dashboard":
                self.logger.info(self.brain.dashboard_data())
                continue

            if cmd == "report":
                self.logger.info(self.brain.report())
                continue

            if cmd == "export-report":
                self.logger.info(self.brain.export_report())
                continue

            if cmd == "export-report-md":
                self.logger.info(self.brain.export_markdown_report())
                continue

            if cmd == "export-obsidian":
                self.logger.info(self.brain.export_obsidian_report())
                continue

            if cmd == "backup":
                self.logger.info(self.brain.create_backup())
                continue

            if cmd == "backups":
                self.logger.info(self.brain.list_backups())
                continue

            if cmd == "snapshot":
                self.logger.info(self.brain.create_snapshot())
                continue

            if cmd == "snapshots":
                self.logger.info(self.brain.list_snapshots())
                continue

            if cmd == "memory":
                self.logger.info(self.brain.memory.dump())
                continue

            if cmd.startswith("memory-key "):
                key = cmd.replace("memory-key ", "", 1).strip()
                self.logger.info(self.brain.memory.get(key))
                continue

            if cmd.startswith("chat "):
                text = cmd.replace("chat ", "", 1).strip()
                self.logger.info(self.brain.chat(text))
                continue

            if cmd.startswith("jarvis "):
                text = cmd.replace("jarvis ", "", 1).strip()
                self.logger.info(self.brain.handle_command(text))
                continue

            self.logger.info("unknown command")
