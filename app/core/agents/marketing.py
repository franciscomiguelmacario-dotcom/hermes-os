from app.core.agents.base_agent import BaseAgent


class MarketingAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=7):
        super().__init__(name, memory, logger, bus, brain, priority)

    def tick(self):
        if not self.brain:
            return

        for task in self.brain.tasks.pending():
            title = task["title"].lower()

            if (
                "marketing" in title
                or "ads" in title
                or "anuncio" in title
                or "anúncio" in title
                or "campanha" in title
                or "trafego" in title
                or "tráfego" in title
            ):
                result = {
                    "task": task["title"],
                    "platforms": ["Meta Ads", "TikTok Ads", "Google Ads"],
                    "strategy": [
                        "testar 3 criativos",
                        "validar produto com baixo orçamento",
                        "medir CTR, CPC e conversão",
                        "escalar apenas campanhas lucrativas"
                    ],
                    "status": "marketing_plan_created"
                }

                self.logger.info(f"[marketing] plan created: {task['title']}")
                self.memory.set("last_marketing_plan", result)
                self.brain.tasks.complete(task["id"], result)
