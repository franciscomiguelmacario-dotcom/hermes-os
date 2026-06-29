from app.core.agent import Agent


class ExecutorAgent(Agent):

    def decide(self):
        return {"task": "check_execution"}

    def act(self, data):
        if data:
            self.logger.info(f"[executor] executing: {data}")

    def tick(self):
        decision = self.decide()
        self.act(decision)
