from app.core.agents.base_agent import BaseAgent


class ExecutorAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=5):
        super().__init__(name, memory, logger, bus, brain, priority)

        if self.bus:
            self.bus.subscribe("task.created", self.on_task_created)

    def on_task_created(self, task):
        self.logger.info(f"[executor] task received: {task}")

    def tick(self):
        if not self.brain:
            return

        pending = self.brain.tasks.pending()

        for task in pending:
            self.logger.info(f"[executor] executing task: {task['title']}")
            self.brain.tasks.complete(task["id"])
