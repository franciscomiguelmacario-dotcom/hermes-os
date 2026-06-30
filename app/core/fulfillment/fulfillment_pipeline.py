from datetime import datetime


class FulfillmentPipeline:

    def __init__(
        self,
        order_manager,
        supplier_api,
        notifications=None,
        memory=None,
        logger=None
    ):
        self.order_manager = order_manager
        self.supplier_api = supplier_api
        self.notifications = notifications
        self.memory = memory
        self.logger = logger

    def submit_order(self, order_id):
        order = self.order_manager.get_order(order_id)

        if not order:
            return {
                "status": "error",
                "message": "order not found"
            }

        if order.get("fulfillment_status") == "fulfilled":
            return {
                "status": "skipped",
                "message": "order already fulfilled",
                "order": order
            }

        result = self.supplier_api.submit_order(order)

        supplier_status = result.get("status")

        self.order_manager.update_order(
            order_id,
            "supplier_submission_status",
            supplier_status
        )

        self.order_manager.update_order(
            order_id,
            "supplier_submission_result",
            result
        )

        self.order_manager.update_order(
            order_id,
            "supplier_submitted_at",
            datetime.now().isoformat()
        )

        if supplier_status == "supplier_order_submitted":
            self.order_manager.update_order(
                order_id,
                "fulfillment_status",
                "supplier_submitted"
            )

            self.order_manager.update_order(
                order_id,
                "status",
                "supplier_submitted"
            )

        if supplier_status == "dry_run_supplier_order_prepared":
            self.order_manager.update_order(
                order_id,
                "status",
                "supplier_dry_run_prepared"
            )

        updated_order = self.order_manager.get_order(order_id)

        pipeline_result = {
            "status": "fulfillment_submission_processed",
            "order_id": int(order_id),
            "supplier_result": result,
            "order": updated_order
        }

        self.record_history("submit_order", pipeline_result)

        return pipeline_result

    def submit_pending_orders(self):
        pending_orders = self.order_manager.pending()
        results = []

        for order in pending_orders:
            results.append(
                self.submit_order(order["id"])
            )

        batch = {
            "status": "pending_orders_submitted_to_supplier",
            "created_at": datetime.now().isoformat(),
            "orders_checked": len(pending_orders),
            "orders_processed": len(results),
            "results": results
        }

        self.record_history("submit_pending_orders", batch)

        return batch

    def mark_tracking(self, order_id, tracking_number):
        order = self.order_manager.get_order(order_id)

        if not order:
            return {
                "status": "error",
                "message": "order not found"
            }

        result = self.order_manager.fulfill_order(
            order_id,
            tracking_number
        )

        if (
            result.get("status") == "order_fulfilled"
            and self.notifications
        ):
            self.notifications.shipping_confirmation(
                result.get("order")
            )

        pipeline_result = {
            "status": "tracking_registered",
            "order_id": int(order_id),
            "tracking_number": tracking_number,
            "result": result
        }

        self.record_history("mark_tracking", pipeline_result)

        return pipeline_result

    def record_history(self, action, result):
        if not self.memory:
            return

        history = self.memory.get("fulfillment_pipeline_history", [])

        history.append({
            "created_at": datetime.now().isoformat(),
            "action": action,
            "result": result
        })

        self.memory.set("fulfillment_pipeline_history", history)

    def history(self):
        if not self.memory:
            return []

        return self.memory.get("fulfillment_pipeline_history", [])
