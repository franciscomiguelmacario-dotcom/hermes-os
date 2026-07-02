from app.core.agents.base_agent import BaseAgent
from app.core.business.dropshipping_business import DropshippingBusinessToolkit


class OrganicTrafficAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=7):
        super().__init__(name, memory, logger, bus, brain, priority)
        self.toolkit = DropshippingBusinessToolkit()

        if self.bus:
            self.bus.subscribe("task.created", self.on_task_created)
            self.bus.subscribe(
                "dropshipping.organic.requested",
                self.on_organic_requested
            )
            self.bus.subscribe(
                "organic.requested",
                self.on_organic_requested
            )

    def log(self, message):
        if self.logger:
            self.logger.info(message)

    def matches_task(self, task):
        title = self.toolkit.normalize(task.get("title") if isinstance(task, dict) else task)

        terms = [
            "organico",
            "organic",
            "trafego organico",
            "conteudo",
            "content",
            "seo",
            "post",
            "posts",
            "calendario",
            "tiktok",
            "reels",
            "shorts",
            "youtube shorts",
            "instagram"
        ]

        paid_only_terms = [
            "tiktok ads",
            "meta ads",
            "facebook ads",
            "google ads",
            "trafego pago",
            "campanha paga"
        ]

        if any(term in title for term in paid_only_terms):
            return False

        return any(term in title for term in terms)

    def all_candidates(self):
        candidates = self.memory.get("product_candidates", [])
        return candidates if isinstance(candidates, list) else []

    def resolve_product(self, product_id=None, product=None):
        if isinstance(product, dict):
            return product

        candidates = self.all_candidates()

        if product_id is not None:
            product_id = str(product_id)

            for candidate in candidates:
                if str(candidate.get("id")) == product_id:
                    return candidate

            if self.brain and hasattr(self.brain, "store_products"):
                for item in self.brain.store_products():
                    if str(item.get("id")) == product_id:
                        return item

            if self.brain and hasattr(self.brain, "supplier_products"):
                for item in self.brain.supplier_products():
                    if str(item.get("id")) == product_id:
                        return item

        best_candidate = self.memory.get("best_product_candidate")

        if isinstance(best_candidate, dict):
            return best_candidate

        last_research = self.memory.get("last_product_research", {})
        if isinstance(last_research, dict) and isinstance(last_research.get("best_candidate"), dict):
            return last_research["best_candidate"]

        if candidates:
            return candidates[0]

        if self.brain and hasattr(self.brain, "store_products"):
            products = self.brain.store_products()
            if products:
                return products[0]

        if self.brain and hasattr(self.brain, "supplier_products"):
            products = self.brain.supplier_products()
            if products:
                return products[0]

        return self.toolkit.seed_products("produto vencedor")[0]

    def save_plan(self, plan):
        plans = self.memory.get("organic_content_plans", [])

        if not isinstance(plans, list):
            plans = []

        plan["id"] = max([int(item.get("id", 0)) for item in plans] + [0]) + 1
        plans.append(plan)

        self.memory.set("organic_content_plans", plans)
        self.memory.set("last_organic_plan", plan)

        return plan

    def create_content_plan(
        self,
        product_id=None,
        product=None,
        days=7,
        task=None
    ):
        selected = self.resolve_product(product_id, product)
        plan = self.toolkit.build_organic_plan(selected, days)
        plan["task"] = task.get("title") if isinstance(task, dict) else None

        plan = self.save_plan(plan)

        self.log(f"[organic] plan created: {plan['product']['name']}")

        if self.bus:
            self.bus.emit("dropshipping.organic.completed", plan)

        return plan

    def complete_task(self, task, result):
        if self.brain and hasattr(self.brain, "tasks") and isinstance(task, dict):
            self.brain.tasks.complete(task["id"], result)

    def on_task_created(self, task):
        if isinstance(task, dict) and self.matches_task(task):
            result = self.create_content_plan(task=task)
            self.complete_task(task, result)

    def on_organic_requested(self, payload):
        if not isinstance(payload, dict):
            payload = {"product_id": payload}

        result = self.create_content_plan(
            product_id=payload.get("product_id"),
            product=payload.get("product"),
            days=payload.get("days", 7),
            task=payload.get("task")
        )

        task = payload.get("task")
        if task:
            self.complete_task(task, result)

        return result

    def tick(self):
        if not self.brain:
            return

        for task in list(self.brain.tasks.pending()):
            if self.matches_task(task):
                result = self.create_content_plan(task=task)
                self.complete_task(task, result)
