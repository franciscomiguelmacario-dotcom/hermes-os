from app.core.agent import Agent


class AnalyzerAgent(Agent):

    def decide(self):
        return {"task": "analyze_system"}

    def act(self, data):
        if data:
            self.logger.info(f"[analyzer] analyzing: {data}")

    def tick(self):
        decision = self.decide()
        self.act(decision)
