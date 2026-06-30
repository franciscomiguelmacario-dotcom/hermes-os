class ProductPublisher:

    def __init__(self, store, memory, logger=None):
        self.store = store
        self.memory = memory
        self.logger = logger

    def get_product(self, product_id):
        for product in self.store.products():
            if product["id"] == int(product_id):
                return product

        return None

    def publish(self, product_id):
        product = self.get_product(product_id)

        if not product:
            return {
                "status": "error",
                "message": "product not found"
            }

        if not product.get("price"):
            return {
                "status": "error",
                "message": "product has no price"
            }

        title = product.get("title", "Produto")
        category = product.get("category") or "produto"

        description = self.generate_description(title, category)

        self.store.update_product(product_id, "description", description)
        self.store.update_product(product_id, "seo_title", title)
        self.store.update_product(
            product_id,
            "seo_description",
            f"{title} com envio rápido e preço competitivo."
        )
        self.store.update_product(product_id, "status", "active")
        self.store.update_product(product_id, "published", True)

        updated = self.get_product(product_id)

        history = self.memory.get("product_publish_history", [])
        history.append(updated)
        self.memory.set("product_publish_history", history)

        return {
            "status": "product_published",
            "product": updated
        }

    def unpublish(self, product_id):
        product = self.get_product(product_id)

        if not product:
            return {
                "status": "error",
                "message": "product not found"
            }

        self.store.update_product(product_id, "status", "draft")
        self.store.update_product(product_id, "published", False)

        return {
            "status": "product_unpublished",
            "product": self.get_product(product_id)
        }

    def generate_description(self, title, category):
        return {
            "headline": title,
            "category": category,
            "benefits": [
                "produto selecionado para venda online",
                "preço calculado com margem de lucro",
                "ideal para testar em campanhas",
                "página preparada para conversão"
            ],
            "cta": "Compra agora antes que esgote."
        }

    def history(self):
        return self.memory.get("product_publish_history", [])
