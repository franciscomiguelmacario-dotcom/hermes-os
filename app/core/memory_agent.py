from app.core.agent import Agent


class MemoryAgent(Agent):

    def decide(self, goal):

        if goal == "ensure_ready":
            status = self.memory.get("system_status")

            if status != "ready":
                return {"action": "set_ready", "value": "ready"}

        return None

    def act(self, data):

        if data and data.get("action") == "set_ready":
            self.logger.info("[memory] system_status=ready")
            self.memory.set("system_status", data["value"])
