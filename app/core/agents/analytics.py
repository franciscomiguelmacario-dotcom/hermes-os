from app.core.agents.base_agent import BaseAgent


class AnalyticsAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=6):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "analytics" in title
                or "metricas" in title
                or "métricas" in title
                or "vendas" in title
                or "lucro" in title
                or "conversao" in title
                or "conversão" in title
                or "kpi" in title
                or "dados" in title
            ):
                result = {
                    "task": task["title"],
                    "metrics": [
                        "vendas totais",
                        "taxa de conversão",
                        "custo por aquisição",
                        "lucro líquido",
                        "ROAS",
                        "CTR",
                        "CPC",
                        "abandono de checkout"
                    ],
                    "actions": [
                        "guardar métricas principais",
                        "identificar gargalos",
                        "comparar campanhas",
                        "recomendar otimizações",
                        "gerar relatório operacional"
                    ],
                    "status": "analytics_plan_created"
                }

                self.logger.info(f"[analytics] plan created: {task['title']}")
                self.memory.set("last_analytics_plan", result)
                self.brain.tasks.complete(task["id"], result)
