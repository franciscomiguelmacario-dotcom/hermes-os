class SupplierConnector:

    def __init__(self, memory, logger=None):
        self.memory = memory
        self.logger = logger

    def config(self):
        return self.memory.get("supplier_config", {
            "platform": "local",
            "supplier_name": None,
            "api_key": None,
            "currency": "EUR"
        })

    def set_value(self, key, value):
        config = self.config()
        config[key] = value
        self.memory.set("supplier_config", config)

        return {
            "status": "supplier_config_saved",
            "supplier_config": config
        }

    def products(self):
        return self.memory.get("supplier_products", [])

    def add_product(
        self,
        title,
        cost=None,
        shipping_days=None,
        supplier_url=None,
        category=None
    ):
        products = self.products()

        product = {
            "id": len(products) + 1,
            "title": title,
            "cost": cost,
            "shipping_days": shipping_days,
            "supplier_url": supplier_url,
            "category": category,
            "status": "available",
            "source": "supplier"
        }

        products.append(product)
        self.memory.set("supplier_products", products)

        return {
            "status": "supplier_product_added",
            "product": product
        }

    def search(self, keyword):
        keyword = keyword.lower().strip()

        results = [
            product for product in self.products()
            if keyword in product.get("title", "").lower()
            or keyword in str(product.get("category", "")).lower()
        ]

        return {
            "status": "ok",
            "keyword": keyword,
            "results": results
        }

    def get_product(self, product_id):
        for product in self.products():
            if product["id"] == int(product_id):
                return product

        return None

    def delete_product(self, product_id):
        products = self.products()

        updated = [
            product for product in products
            if product["id"] != int(product_id)
        ]

        self.memory.set("supplier_products", updated)

        return {
            "status": "supplier_product_deleted",
            "product_id": product_id
        }
