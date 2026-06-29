from app.core.agents.base_agent import BaseAgent


class StrategyAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=9):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "estrategia" in title
                or "estratégia" in title
                or "plano negocio" in title
                or "plano de negocio" in title
                or "plano de negócio" in title
                or "business plan" in title
            ):
                profile = self.brain.business_profile()

                result = {
                    "task": task["title"],
                    "business_profile": profile,
                    "strategy": [
                        "definir produto vencedor alinhado ao nicho",
                        "validar procura antes de investir forte",
                        "testar anúncios com orçamento controlado",
                        "criar conteúdo orgânico diariamente",
                        "medir vendas, lucro e ROAS",
                        "escalar apenas produtos lucrativos"
                    ],
                    "status": "strategy_plan_created"
                }

                self.logger.info(f"[strategy] plan created: {task['title']}")
                self.memory.set("last_strategy_plan", result)
                self.brain.tasks.complete(task["id"], result)
