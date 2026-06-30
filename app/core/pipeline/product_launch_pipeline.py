class ProductLaunchPipeline:

    def __init__(self, importer, publisher, supplier, memory, logger=None):
        self.importer = importer
        self.publisher = publisher
        self.supplier = supplier
        self.memory = memory
        self.logger = logger

    def launch_from_supplier_product(self, supplier_product_id, margin_percent=None):
        imported = self.importer.import_supplier_product(
            supplier_product_id,
            margin_percent
        )

        if imported.get("status") != "product_imported":
            return imported

        store_product = imported.get("store_product")

        if not store_product:
            return {
                "status": "error",
                "message": "store product not created"
            }

        published = self.publisher.publish(store_product["id"])

        result = {
            "status": "product_launched",
            "supplier_product": imported.get("supplier_product"),
            "store_product": published.get("product"),
            "pricing": imported.get("pricing"),
            "publish_result": published
        }

        history = self.memory.get("product_launch_history", [])
        history.append(result)
        self.memory.set("product_launch_history", history)

        return result

    def launch_first_match(self, keyword, margin_percent=None):
        search = self.supplier.search(keyword)
        results = search.get("results", [])

        if not results:
            return {
                "status": "error",
                "message": "no supplier product found",
                "keyword": keyword
            }

        first = results[0]

        return self.launch_from_supplier_product(
            first["id"],
            margin_percent
        )

    def history(self):
        return self.memory.get("product_launch_history", [])
