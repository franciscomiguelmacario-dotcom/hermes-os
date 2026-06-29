from app.core.agents.base_agent import BaseAgent


class OrganicTrafficAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=6):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "organico" in title
                or "orgânico" in title
                or "seo" in title
                or "conteudo" in title
                or "conteúdo" in title
                or "tiktok" in title
                or "instagram" in title
                or "trafego organico" in title
                or "tráfego orgânico" in title
            ):
                result = {
                    "task": task["title"],
                    "channels": ["TikTok", "Instagram Reels", "YouTube Shorts", "SEO Blog"],
                    "plan": [
                        "publicar 2 vídeos curtos por dia",
                        "usar produto em demonstração real",
                        "testar hooks nos primeiros 3 segundos",
                        "reaproveitar conteúdo em várias plataformas",
                        "guardar métricas de visualização e cliques"
                    ],
                    "status": "organic_plan_created"
                }

                self.logger.info(f"[organic] plan created: {task['title']}")
                self.memory.set("last_organic_plan", result)
                self.brain.tasks.complete(task["id"], result)
