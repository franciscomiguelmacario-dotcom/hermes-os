import json
import os
from datetime import datetime


class ReportEngine:

    def __init__(self, memory, tasks):
        self.memory = memory
        self.tasks = tasks
        self.path = "data/reports"
        self.obsidian_path = os.getenv("HERMES_OBSIDIAN_PATH", "data/obsidian/Hermes")

        os.makedirs(self.path, exist_ok=True)
        os.makedirs(self.obsidian_path, exist_ok=True)

    def business_report(self):
        all_tasks = self.tasks.all()

        return {
            "created_at": datetime.now().isoformat(),
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

    def markdown_content(self):
        report = self.business_report()

        return f"""# Hermes Business Report

Created: {report["created_at"]}

## Tasks

- Total: {report["tasks_total"]}
- Done: {report["tasks_done"]}
- Pending: {report["tasks_pending"]}

## Product Research

{report["product_research"]}

## Supplier

{report["supplier"]}

## Marketing

{report["marketing"]}

## Organic Traffic

{report["organic"]}

## Design

{report["design"]}

## Store Operations

{report["store_ops"]}

## Fulfillment

{report["fulfillment"]}

## Support

{report["support"]}

## Analytics

{report["analytics"]}
"""

    def export_business_report(self):
        report = self.business_report()

        filename = f"business_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.path, filename)

        with open(filepath, "w") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        return {"status": "exported", "file": filepath}

    def export_markdown_report(self):
        filename = f"business_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.path, filename)

        with open(filepath, "w") as f:
            f.write(self.markdown_content())

        return {"status": "exported", "file": filepath}

    def export_obsidian_report(self):
        filename = f"Hermes Business Report {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.md"
        filepath = os.path.join(self.obsidian_path, filename)

        with open(filepath, "w") as f:
            f.write(self.markdown_content())

        return {"status": "exported_to_obsidian", "file": filepath}
