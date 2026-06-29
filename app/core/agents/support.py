from app.core.agents.base_agent import BaseAgent


class SupportAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=7):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "cliente" in title
                or "suporte" in title
                or "support" in title
                or "email cliente" in title
                or "mensagem cliente" in title
                or "reclamação" in title
                or "duvida" in title
                or "dúvida" in title
                or "atendimento" in title
            ):
                result = {
                    "task": task["title"],
                    "response_plan": [
                        "identificar problema do cliente",
                        "verificar estado do pedido",
                        "responder com tom profissional",
                        "oferecer solução clara",
                        "guardar histórico do atendimento",
                        "encaminhar caso crítico para revisão manual"
                    ],
                    "status": "support_plan_created"
                }

                self.logger.info(f"[support] plan created: {task['title']}")
                self.memory.set("last_support_plan", result)
                self.brain.tasks.complete(task["id"], result)
