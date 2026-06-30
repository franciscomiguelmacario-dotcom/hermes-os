class StoreConnector:

    def __init__(self, memory, logger=None):
        self.memory = memory
        self.logger = logger

    def config(self):
        return self.memory.get("store_config", {
            "platform": "local",
            "store_url": None,
            "api_key": None,
            "api_secret": None,
            "currency": "EUR"
        })

    def set_value(self, key, value):
        config = self.config()
        config[key] = value
        self.memory.set("store_config", config)

        return {
            "status": "store_config_saved",
            "store_config": config
        }

    def products(self):
        return self.memory.get("store_products", [])

    def create_product(self, title, price=None, cost=None):
        products = self.products()

        product = {
            "id": len(products) + 1,
            "title": title,
            "price": price,
            "cost": cost,
            "status": "draft",
            "source": "hermes"
        }

        products.append(product)
        self.memory.set("store_products", products)

        return {
            "status": "product_created",
            "product": product
        }

    def update_product(self, product_id, key, value):
        products = self.products()

        for product in products:
            if product["id"] == int(product_id):
                product[key] = value
                self.memory.set("store_products", products)

                return {
                    "status": "product_updated",
                    "product": product
                }

        return {
            "status": "error",
            "message": "product not found"
        }

    def delete_product(self, product_id):
        products = self.products()

        updated = [
            product for product in products
            if product["id"] != int(product_id)
        ]

        self.memory.set("store_products", updated)

        return {
            "status": "product_deleted",
            "product_id": product_id
        }
