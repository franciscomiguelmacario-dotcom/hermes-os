class ProductLaunchPipeline:

    def __init__(self, importer, publisher, supplier, memory, logger=None, scoring=None):
        self.importer = importer
        self.publisher = publisher
        self.supplier = supplier
        self.memory = memory
        self.logger = logger
        self.scoring = scoring

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

    def launch_best_product(self, margin_percent=None):
        if not self.scoring:
            return {
                "status": "error",
                "message": "scoring engine not available"
            }

        best_result = self.scoring.best_product()

        if best_result.get("status") != "best_product_selected":
            return best_result

        best = best_result.get("best", {})
        product = best.get("product")

        if not product:
            return {
                "status": "error",
                "message": "best product not found"
            }

        launched = self.launch_from_supplier_product(
            product["id"],
            margin_percent
        )

        return {
            "status": "best_product_launched",
            "score": best,
            "launch": launched
        }

    def history(self):
        return self.memory.get("product_launch_history", [])
