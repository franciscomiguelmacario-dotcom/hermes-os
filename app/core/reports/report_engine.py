class ReportEngine:

    def __init__(self, memory, tasks):
        self.memory = memory
        self.tasks = tasks

    def business_report(self):
        all_tasks = self.tasks.all()

        return {
            "tasks_total": len(all_tasks),
            "tasks_done": len([t for t in all_tasks if t["status"] == "done"]),
            "tasks_pending": len([t for t in all_tasks if t["status"] == "pending"]),
            "product_research": self.memory.get("last_product_research"),
            "supplier": self.memory.get("last_supplier_plan"),
            "marketing": self.memory.get("last_marketing_plan"),
            "organic": self.memory.get("last_organic_plan"),
            "design": self.memory.get("last_design_plan"),
            "store_ops": self.memory.get("last_store_ops_plan"),
            "fulfillment": self.memory.get("last_fulfillment_plan"),
            "support": self.memory.get("last_support_plan"),
            "analytics": self.memory.get("last_analytics_plan")
        }
