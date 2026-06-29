from app.core.agents.base_agent import BaseAgent


class DesignAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=6):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "design" in title
                or "loja" in title
                or "site" in title
                or "landing page" in title
                or "produto page" in title
                or "pagina produto" in title
                or "página produto" in title
            ):
                result = {
                    "task": task["title"],
                    "focus": [
                        "visual moderno",
                        "confiança do cliente",
                        "conversão",
                        "velocidade",
                        "mobile first"
                    ],
                    "recommendations": [
                        "usar hero section clara",
                        "mostrar benefício principal acima da dobra",
                        "adicionar prova social",
                        "usar botão CTA visível",
                        "simplificar checkout",
                        "melhorar imagens do produto"
                    ],
                    "status": "design_plan_created"
                }

                self.logger.info(f"[design] plan created: {task['title']}")
                self.memory.set("last_design_plan", result)
                self.brain.tasks.complete(task["id"], result)
