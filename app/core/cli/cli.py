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
                        "jarvis <texto>",
                        "ask <texto>",
                        "chat <texto>",
                        "health",
                        "status",
                        "memory",
                        "memory-key <key>",
                        "backup",
                        "backups",
                        "restore-backup <filename>",
                        "snapshot",
                        "snapshots",
                        "restore-snapshot <filename>",
                        "business",
                        "set-business <key> <value>",
                        "store",
                        "set-store <key> <value>",
                        "supplier",
                        "set-supplier <key> <value>",
                        "supplier-products",
                        "add-supplier-product <title> | <cost> | <shipping_days> | <url> | <category>",
                        "search-supplier <keyword>",
                        "delete-supplier-product <id>",
                        "score-suppliers",
                        "best-supplier-product",
                        "pricing",
                        "set-pricing <key> <value>",
                        "price <cost> <shipping> <margin_percent>",
                        "products",
                        "create-product <title> | <price> | <cost>",
                        "product <id>",
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
                        "set-obsidian-path <path>",
                        "voice",
                        "set-voice <key> <value>",
                        "say <texto>",
                        "jarvis-say <texto>",
                        "listen",
                        "jarvis-listen",
                        "listen-config",
                        "set-listen <key> <value>",
                        "jarvis-mode",
                        "jarvis-mode <cycles>",
                        "learn",
                        "patterns",
                        "history <agent>",
                        "priority <agent> <number>",
                        "run <texto>",
                        "exit"
                    ]
                })
                continue

            if cmd.startswith("jarvis "):
                text = cmd.replace("jarvis ", "", 1).strip()
                self.logger.info(self.brain.handle_command(text))
                continue

            if cmd.startswith("ask "):
                text = cmd.replace("ask ", "", 1).strip()
                self.logger.info(self.brain.handle_command(text))
                continue

            if cmd.startswith("chat "):
                text = cmd.replace("chat ", "", 1).strip()
                self.logger.info(self.brain.chat(text))
                continue

            if cmd.startswith("jarvis-say "):
                text = cmd.replace("jarvis-say ", "", 1).strip()
                self.logger.info(self.brain.handle_command_voice(text))
                continue

            if cmd.startswith("say "):
                text = cmd.replace("say ", "", 1).strip()
                self.logger.info(self.brain.speak(text))
                continue

            if cmd == "voice":
                self.logger.info(self.brain.voice_config())
                continue

            if cmd.startswith("set-voice "):
                parts = cmd.split(" ", 2)

                if len(parts) < 3:
                    self.logger.info("usage: set-voice <key> <value>")
                    continue

                _, key, value = parts
                self.logger.info(self.brain.set_voice_value(key, value))
                continue

            if cmd == "listen-config":
                self.logger.info(self.brain.listen_config())
                continue

            if cmd.startswith("set-listen "):
                parts = cmd.split(" ", 2)

                if len(parts) < 3:
                    self.logger.info("usage: set-listen <key> <value>")
                    continue

                _, key, value = parts
                self.logger.info(self.brain.set_listen_value(key, value))
                continue

            if cmd == "listen":
                self.logger.info("listening...")
                self.logger.info(self.brain.listen_once())
                continue

            if cmd == "jarvis-listen":
                self.logger.info("listening...")
                self.logger.info(self.brain.listen_and_handle())
                continue

            if cmd.startswith("jarvis-mode"):
                parts = cmd.split(" ")

                cycles = 10
                if len(parts) == 2:
                    cycles = int(parts[1])

                self.logger.info(self.brain.start_jarvis_mode(cycles=cycles))
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

            if cmd == "backup":
                self.logger.info(self.brain.create_backup())
                continue

            if cmd == "backups":
                self.logger.info(self.brain.list_backups())
                continue

            if cmd.startswith("restore-backup "):
                filename = cmd.replace("restore-backup ", "", 1).strip()
                self.logger.info(self.brain.restore_backup(filename))
                continue

            if cmd == "snapshot":
                self.logger.info(self.brain.create_snapshot())
                continue

            if cmd == "snapshots":
                self.logger.info(self.brain.list_snapshots())
                continue

            if cmd.startswith("restore-snapshot "):
                filename = cmd.replace("restore-snapshot ", "", 1).strip()
                self.logger.info(self.brain.restore_snapshot(filename))
                continue

            if cmd == "memory":
                self.logger.info(self.brain.memory.dump())
                continue

            if cmd.startswith("memory-key "):
                key = cmd.replace("memory-key ", "", 1).strip()
                self.logger.info(self.brain.memory.get(key))
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

            if cmd.startswith("delete-supplier-product "):
                product_id = cmd.replace("delete-supplier-product ", "", 1).strip()
                self.logger.info(self.brain.delete_supplier_product(product_id))
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

            if cmd.startswith("set-pricing "):
                parts = cmd.split(" ", 2)

                if len(parts) < 3:
                    self.logger.info("usage: set-pricing <key> <value>")
                    continue

                _, key, value = parts
                self.logger.info(self.brain.set_pricing_value(key, value))
                continue

            if cmd.startswith("price "):
                parts = cmd.split(" ")

                cost = parts[1] if len(parts) > 1 else 0
                shipping = parts[2] if len(parts) > 2 else 0
                margin = parts[3] if len(parts) > 3 else None

                self.logger.info(
                    self.brain.calculate_price(cost, shipping, margin)
                )
                continue

            if cmd.startswith("launch-best-product"):
                parts = cmd.split(" ")
                margin = parts[1] if len(parts) > 1 else None

                self.logger.info(
                    self.brain.launch_best_product(margin)
                )
                continue

            if cmd.startswith("launch-product-search "):
                raw = cmd.replace("launch-product-search ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                keyword = parts[0]
                margin = parts[1] if len(parts) > 1 else None

                self.logger.info(
                    self.brain.launch_product_search(keyword, margin)
                )
                continue

            if cmd.startswith("launch-product "):
                parts = cmd.split(" ")

                supplier_product_id = parts[1] if len(parts) > 1 else None
                margin = parts[2] if len(parts) > 2 else None

                if not supplier_product_id:
                    self.logger.info("usage: launch-product <supplier_product_id> <margin_percent>")
                    continue

                self.logger.info(
                    self.brain.launch_product(
                        supplier_product_id,
                        margin
                    )
                )
                continue

            if cmd == "launch-history":
                self.logger.info(self.brain.product_launch_history())
                continue

            if cmd.startswith("import-product-search "):
                raw = cmd.replace("import-product-search ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                keyword = parts[0]
                margin = parts[1] if len(parts) > 1 else None

                self.logger.info(
                    self.brain.import_supplier_search(keyword, margin)
                )
                continue

            if cmd.startswith("import-product "):
                parts = cmd.split(" ")

                supplier_product_id = parts[1] if len(parts) > 1 else None
                margin = parts[2] if len(parts) > 2 else None

                if not supplier_product_id:
                    self.logger.info("usage: import-product <supplier_product_id> <margin_percent>")
                    continue

                self.logger.info(
                    self.brain.import_supplier_product(
                        supplier_product_id,
                        margin
                    )
                )
                continue

            if cmd == "import-history":
                self.logger.info(self.brain.product_import_history())
                continue

            if cmd.startswith("product "):
                product_id = cmd.replace("product ", "", 1).strip()
                self.logger.info(self.brain.product_detail(product_id))
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

            if cmd == "products":
                self.logger.info(self.brain.store_products())
                continue

            if cmd.startswith("create-product "):
                raw = cmd.replace("create-product ", "", 1).strip()
                parts = [p.strip() for p in raw.split("|")]

                title = parts[0]
                price = parts[1] if len(parts) > 1 else None
                cost = parts[2] if len(parts) > 2 else None

                self.logger.info(
                    self.brain.create_store_product(title, price, cost)
                )
                continue

            if cmd.startswith("update-product "):
                parts = cmd.split(" ", 3)

                if len(parts) < 4:
                    self.logger.info("usage: update-product <id> <key> <value>")
                    continue

                _, product_id, key, value = parts
                self.logger.info(
                    self.brain.update_store_product(product_id, key, value)
                )
                continue

            if cmd.startswith("delete-product "):
                product_id = cmd.replace("delete-product ", "", 1).strip()
                self.logger.info(self.brain.delete_store_product(product_id))
                continue

            if cmd == "tasks":
                self.logger.info(self.brain.tasks.all())
                continue

            if cmd == "clear-tasks":
                self.logger.info(self.brain.clear_tasks())
                continue

            if cmd.startswith("task "):
                title = cmd[5:]
                task = self.brain.create_task(title)
                self.logger.info(task)
                continue

            if cmd == "workflows":
                self.logger.info(self.brain.workflows.list())
                continue

            if cmd.startswith("workflow "):
                name = cmd[9:]
                result = self.brain.run_workflow(name)
                self.logger.info(result)
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

            if cmd.startswith("set-obsidian-path "):
                path = cmd.replace("set-obsidian-path ", "", 1).strip()
                self.logger.info(self.brain.set_obsidian_path(path))
                continue

            if cmd == "learn":
                self.logger.info(self.brain.learning.all())
                continue

            if cmd == "patterns":
                self.logger.info(self.brain.memory.get("input_patterns", {}))
                continue

            if cmd.startswith("history "):
                _, agent = cmd.split(" ", 1)
                self.logger.info(self.brain.learning.history(agent))
                continue

            if cmd.startswith("priority "):
                _, name, value = cmd.split(" ", 2)
                ok = self.brain.set_priority(name, value)
                self.logger.info("priority updated" if ok else "agent not found")
                continue

            if cmd.startswith("run "):
                data = cmd[4:]
                result = self.brain.process(data)
                self.logger.info(result)
                continue

            self.logger.info("unknown command")
