from app.core.agents.base_agent import BaseAgent


class SupplierAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=7):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "fornecedor" in title
                or "supplier" in title
                or "aliexpress" in title
                or "cj dropshipping" in title
                or "envio" in title
                or "shipping" in title
                or "prazo" in title
            ):
                result = {
                    "task": task["title"],
                    "checks": [
                        "verificar preço do fornecedor",
                        "validar tempo de envio",
                        "confirmar avaliações do produto",
                        "analisar margem de lucro",
                        "verificar política de devolução",
                        "guardar fornecedor recomendado"
                    ],
                    "status": "supplier_plan_created"
                }

                self.logger.info(f"[supplier] plan created: {task['title']}")
                self.memory.set("last_supplier_plan", result)
                self.brain.tasks.complete(task["id"], result)
