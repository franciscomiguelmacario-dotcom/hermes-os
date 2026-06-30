class ProductScoring:

    def __init__(self, supplier, memory, logger=None):
        self.supplier = supplier
        self.memory = memory
        self.logger = logger

    def score_product(self, product):
        score = 0
        reasons = []

        title = str(product.get("title", "")).lower()
        cost = float(product.get("cost") or 0)
        shipping_days = int(product.get("shipping_days") or 99)

        if cost > 0 and cost <= 20:
            score += 25
            reasons.append("baixo custo")

        if shipping_days <= 10:
            score += 25
            reasons.append("envio rápido")

        if any(word in title for word in ["smart", "inteligente", "led", "portable", "mini", "wireless"]):
            score += 20
            reasons.append("potencial viral")

        if product.get("category"):
            score += 10
            reasons.append("categoria definida")

        if product.get("supplier_url"):
            score += 10
            reasons.append("fornecedor com link")

        if score >= 70:
            verdict = "winner_candidate"
        elif score >= 45:
            verdict = "test_candidate"
        else:
            verdict = "weak_candidate"

        return {
            "product": product,
            "score": score,
            "verdict": verdict,
            "reasons": reasons
        }

    def score_all(self):
        products = self.supplier.products()

        scored = [
            self.score_product(product)
            for product in products
        ]

        scored = sorted(
            scored,
            key=lambda item: item["score"],
            reverse=True
        )

        self.memory.set("last_product_scores", scored)

        return {
            "status": "scored",
            "products": scored
        }

    def best_product(self):
        scored = self.score_all().get("products", [])

        if not scored:
            return {
                "status": "error",
                "message": "no supplier products available"
            }

        best = scored[0]
        self.memory.set("best_supplier_product", best)

        return {
            "status": "best_product_selected",
            "best": best
        }
