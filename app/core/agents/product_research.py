from app.core.agents.base_agent import BaseAgent
from app.core.business.dropshipping_business import DropshippingBusinessToolkit


class ProductResearchAgent(BaseAgent):

    def __init__(self, name, memory, logger, bus, brain=None, priority=8):
        super().__init__(name, memory, logger, bus, brain, priority)
        self.toolkit = DropshippingBusinessToolkit()

        if self.bus:
            self.bus.subscribe("task.created", self.on_task_created)
            self.bus.subscribe(
                "dropshipping.product_research.requested",
                self.on_research_requested
            )
            self.bus.subscribe(
                "product_research.requested",
                self.on_research_requested
            )

    def log(self, message):
        if self.logger:
            self.logger.info(message)

    def matches_task(self, task):
        title = self.toolkit.normalize(task.get("title") if isinstance(task, dict) else task)

        terms = [
            "produto vencedor",
            "winning product",
            "product research",
            "pesquisar produto",
            "procurar produto",
            "validar produto",
            "produto para vender",
            "produto viral",
            "produto"
        ]

        blockers = [
            "campanha",
            "ads",
            "anuncio",
            "marketing",
            "conteudo",
            "trafego organico",
            "organico"
        ]

        if any(blocker in title for blocker in blockers):
            return False

        return any(term in title for term in terms)

    def business_niche(self):
        if self.brain and hasattr(self.brain, "business_profile"):
            profile = self.brain.business_profile()

            if isinstance(profile, dict):
                return profile.get("niche")

        return None

    def source_products(self, products=None):
        if isinstance(products, list) and products:
            return products

        if self.brain and hasattr(self.brain, "supplier_products"):
            supplier_products = self.brain.supplier_products()

            if supplier_products:
                return supplier_products

        if self.brain and hasattr(self.brain, "store_products"):
            store_products = self.brain.store_products()

            if store_products:
                return store_products

        return []

    def find_existing_candidate(self, saved, candidate):
        candidate_supplier_id = candidate.get("supplier_product_id")
        candidate_name = self.toolkit.normalize(candidate.get("name"))
        candidate_category = self.toolkit.normalize(candidate.get("category"))

        for item in saved:
            supplier_id = item.get("supplier_product_id")

            if candidate_supplier_id and supplier_id == candidate_supplier_id:
                return item

            item_name = self.toolkit.normalize(item.get("name"))
            item_category = self.toolkit.normalize(item.get("category"))

            if item_name == candidate_name and item_category == candidate_category:
                return item

        return None

    def save_candidates(self, candidates):
        saved = self.memory.get("product_candidates", [])

        if not isinstance(saved, list):
            saved = []

        next_id = max([int(item.get("id", 0)) for item in saved] + [0]) + 1
        processed = []

        for candidate in candidates:
            existing = self.find_existing_candidate(saved, candidate)

            if existing:
                candidate["id"] = existing["id"]
                candidate["updated_at"] = candidate["created_at"]
                existing.update(candidate)
                processed.append(existing)
            else:
                candidate["id"] = next_id
                next_id += 1
                saved.append(candidate)
                processed.append(candidate)

        saved = sorted(
            saved,
            key=lambda item: int(item.get("score") or 0),
            reverse=True
        )

        self.memory.set("product_candidates", saved)

        return processed, saved

    def save_history(self, result):
        history = self.memory.get("product_research_history", [])

        if not isinstance(history, list):
            history = []

        history.append(result)
        self.memory.set("product_research_history", history[-30:])

    def research_products(self, query=None, niche=None, products=None, task=None):
        query = query or "produto vencedor"
        niche = niche or self.business_niche()

        source_products = self.source_products(products)

        if not source_products:
            source_products = self.toolkit.seed_products(query, niche)

        candidates = [
            self.toolkit.build_candidate(
                product,
                query=query,
                niche=niche,
                source="product_research"
            )
            for product in source_products
        ]

        processed, all_candidates = self.save_candidates(candidates)

        best_candidate = None
        if all_candidates:
            best_candidate = all_candidates[0]
            self.memory.set("best_product_candidate", best_candidate)

        result = {
            "status": "product_research_completed",
            "task": task.get("title") if isinstance(task, dict) else None,
            "query": query,
            "niche": niche,
            "source_products": len(source_products),
            "candidates": processed,
            "best_candidate": best_candidate,
            "criteria": [
                "demand",
                "low_competition",
                "margin",
                "viral_potential",
                "shipping"
            ],
            "next_steps": [
                "validar fornecedor e prazo de envio",
                "preparar criativos de teste",
                "criar plano de trafego pago",
                "criar plano de conteudo organico"
            ]
        }

        self.memory.set("last_product_research", result)
        self.save_history(result)
        self.log(f"[product_research] completed: {query}")

        if self.bus:
            self.bus.emit("dropshipping.product_research.completed", result)

        return result

    def complete_task(self, task, result):
        if self.brain and hasattr(self.brain, "tasks") and isinstance(task, dict):
            self.brain.tasks.complete(task["id"], result)

    def on_task_created(self, task):
        if isinstance(task, dict) and self.matches_task(task):
            result = self.research_products(query=task.get("title"), task=task)
            self.complete_task(task, result)

    def on_research_requested(self, payload):
        if not isinstance(payload, dict):
            payload = {"query": payload}

        result = self.research_products(
            query=payload.get("query") or payload.get("title"),
            niche=payload.get("niche"),
            products=payload.get("products"),
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
                result = self.research_products(
                    query=task.get("title"),
                    task=task
                )
                self.complete_task(task, result)
