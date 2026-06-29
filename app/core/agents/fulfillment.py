from app.core.agents.base_agent import BaseAgent


class FulfillmentAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=7):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "fulfillment" in title
                or "tracking" in title
                or "processar pedido" in title
                or "atualizar pedido" in title
                or "encomenda enviada" in title
                or "devolução" in title
                or "reembolso" in title
                or "pos-venda" in title
                or "pós-venda" in title
            ):
                result = {
                    "task": task["title"],
                    "actions": [
                        "confirmar pagamento",
                        "enviar pedido ao fornecedor",
                        "guardar número de tracking",
                        "atualizar estado da encomenda",
                        "notificar cliente",
                        "monitorizar entrega",
                        "tratar devolução ou reembolso se necessário"
                    ],
                    "status": "fulfillment_plan_created"
                }

                self.logger.info(f"[fulfillment] plan created: {task['title']}")
                self.memory.set("last_fulfillment_plan", result)
                self.brain.tasks.complete(task["id"], result)
