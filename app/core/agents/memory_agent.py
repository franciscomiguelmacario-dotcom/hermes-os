from app.core.agent import Agent


class MemoryAgent(Agent):

    def decide(self):
        status = self.memory.get("system_status")

        if status != "ready":
            return {"action": "set_ready", "value": "ready"}

        return None

    def act(self, data):

        if data["action"] == "set_ready":
            self.logger.info(f"[memory] setting: {data}")
            self.memory.set("system_status", data["value"])
