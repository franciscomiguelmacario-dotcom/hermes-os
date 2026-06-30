class ProductImporter:

    def __init__(self, store, supplier, pricing, memory, logger=None):
        self.store = store
        self.supplier = supplier
        self.pricing = pricing
        self.memory = memory
        self.logger = logger

    def import_supplier_product(self, supplier_product_id, margin_percent=None):
        supplier_product = self.supplier.get_product(supplier_product_id)

        if not supplier_product:
            return {
                "status": "error",
                "message": "supplier product not found"
            }

        cost = supplier_product.get("cost") or 0

        price_result = self.pricing.calculate(
            cost=cost,
            shipping=0,
            margin_percent=margin_percent
        )

        if price_result.get("status") != "price_calculated":
            return price_result

        created = self.store.create_product(
            title=supplier_product.get("title"),
            price=price_result.get("recommended_price"),
            cost=cost
        )

        product = created.get("product")

        self.store.update_product(product["id"], "supplier_product_id", supplier_product.get("id"))
        self.store.update_product(product["id"], "supplier_url", supplier_product.get("supplier_url"))
        self.store.update_product(product["id"], "category", supplier_product.get("category"))
        self.store.update_product(product["id"], "shipping_days", supplier_product.get("shipping_days"))
        self.store.update_product(product["id"], "pricing", price_result)
        self.store.update_product(product["id"], "status", "draft")

        imported = self.store.update_product(
            product["id"],
            "import_status",
            "imported_from_supplier"
        )

        history = self.memory.get("product_import_history", [])
        history.append({
            "supplier_product": supplier_product,
            "store_product": imported.get("product"),
            "pricing": price_result
        })
        self.memory.set("product_import_history", history)

        return {
            "status": "product_imported",
            "supplier_product": supplier_product,
            "store_product": imported.get("product"),
            "pricing": price_result
        }

    def import_first_match(self, keyword, margin_percent=None):
        search = self.supplier.search(keyword)
        results = search.get("results", [])

        if not results:
            return {
                "status": "error",
                "message": "no supplier product found",
                "keyword": keyword
            }

        first = results[0]

        return self.import_supplier_product(
            first["id"],
            margin_percent
        )

    def history(self):
        return self.memory.get("product_import_history", [])
