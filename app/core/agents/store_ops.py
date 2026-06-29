from app.core.agents.base_agent import BaseAgent


class StoreOpsAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=6):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "loja" in title
                or "store" in title
                or "produto na loja" in title
                or "checkout" in title
                or "stock" in title
                or "preço" in title
                or "pedido" in title
                or "encomenda" in title
                or "dropshipping" in title
            ):
                result = {
                    "task": task["title"],
                    "actions": [
                        "validar produto",
                        "definir preço com margem",
                        "preparar página de produto",
                        "verificar checkout",
                        "monitorizar pedidos",
                        "guardar dados operacionais"
                    ],
                    "status": "store_ops_plan_created"
                }

                self.logger.info(f"[store_ops] plan created: {task['title']}")
                self.memory.set("last_store_ops_plan", result)
                self.brain.tasks.complete(task["id"], result)
