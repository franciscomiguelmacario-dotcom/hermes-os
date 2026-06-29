from app.core.agent_loader import AgentLoader


class Brain:

    def __init__(self, events=None, logger=None, memory=None):
        self.events = events
        self.logger = logger
        self.memory = memory

        loader = AgentLoader(self.logger)
        self.agents = loader.load(self.memory, self.logger)

        for agent in self.agents.values():
            if hasattr(agent, "start"):
                agent.start()

        if self.events:
            self.events.subscribe("system.start", self.on_system_start)

    def on_system_start(self, data):
        self.logger.info("Brain ativado no arranque")
        action = self.decide("system_boot")
        self.execute(action)

    def decide(self, context):

        if context == "system_boot":

            previous = self.memory.get("system_status") if self.memory else None

            if previous == "ready":
                self.logger.success("Brain: sistema já estava pronto")
            else:
                self.logger.success("Brain: primeira inicialização")

            if self.memory:
                self.agents["memory"].act("system_status=ready")
                self.memory.set("system_status", "ready")

            return "SYSTEM_READY"

        return "UNKNOWN"

    def execute(self, action):

        if action == "SYSTEM_READY":

            self.logger.success("Brain executa ação: SYSTEM_READY")

            self.agents["executor"].act({"type": "system_ready"})
            self.agents["analyzer"].act({"status": "system_ready"})

            if self.events:
                self.events.emit("brain.action", {
                    "type": "system_ready",
                    "status": "ok"
                })

            self.run_tick()

    def run_tick(self):

        for agent in self.agents.values():
            if hasattr(agent, "tick"):
                agent.tick()

    def process(self, input_data):
        self.agents["analyzer"].act({"input": input_data})
        return f"Processed: {input_data}"
