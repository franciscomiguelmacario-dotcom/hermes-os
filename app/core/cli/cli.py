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
                        "status",
                        "tasks",
                        "clear-tasks",
                        "task <texto>",
                        "workflows",
                        "workflow dropshipping",
                        "report",
                        "export-report",
                        "export-report-md",
                        "export-obsidian",
                        "set-obsidian-path <path>",
                        "learn",
                        "patterns",
                        "history <agent>",
                        "priority <agent> <number>",
                        "run <texto>",
                        "exit"
                        "autopilot",
                        "autopilot-cycle <steps>",
                 ]
                })
                continue

            if cmd.startswith("autopilot-cycle"):
                parts = cmd.split(" ")

                max_steps = 5
                if len(parts) == 2:
                    max_steps = int(parts[1])

                self.logger.info(self.brain.autopilot_cycle(max_steps))
                continue

            if cmd == "clear-tasks":
                self.logger.info(self.brain.clear_tasks())
                continue

            if cmd == "status":
                self.logger.info({
                    "agents": {
                        name: getattr(agent, "priority", 1)
                        for name, agent in self.brain.agents.items()
                    }
                })
                continue

            if cmd == "tasks":
                self.logger.info(self.brain.tasks.all())
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

            if cmd == "autopilot":
                self.logger.info(self.brain.autopilot_once())


            if cmd == "next-action":
                self.logger.info(self.brain.next_action())
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
