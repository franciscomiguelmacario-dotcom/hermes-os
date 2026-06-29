from app.core.agents.base_agent import BaseAgent


class ProductResearchAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=8):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():

            title = task["title"].lower()

            if "produto" in title or "product" in title or "vencedor" in title:

                result = {
                    "task": task["title"],
                    "status": "analyzed",
                    "criteria": [
                        "high demand",
                        "low competition",
                        "good margin",
                        "viral potential",
                        "easy shipping"
                    ]
                }

                self.logger.info(f"[product_research] analyzed: {task['title']}")

                self.memory.set("last_product_research", result)

                self.brain.tasks.complete(task["id"], result)
