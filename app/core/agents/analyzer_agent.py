from app.core.agent import Agent


class AnalyzerAgent(Agent):

    def decide(self, goal):

        last = self.memory.get("last_input")

        if last:
            return {"action": "analyze", "input": last, "goal": goal}

        return None

    def act(self, data):

        if data and data.get("action") == "analyze":
            self.logger.info(f"[analyzer] input={data['input']}")
