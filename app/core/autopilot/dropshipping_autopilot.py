from datetime import datetime


class DropshippingAutopilot:

    def __init__(
        self,
        launch_pipeline,
        campaign_manager,
        order_manager,
        sales_analytics,
        memory,
        logger=None
    ):
        self.launch_pipeline = launch_pipeline
        self.campaign_manager = campaign_manager
        self.order_manager = order_manager
        self.sales_analytics = sales_analytics
        self.memory = memory
        self.logger = logger

    def active_products(self):
        return self.campaign_manager.active_products()

    def active_campaigns(self):
        return [
            campaign for campaign in self.campaign_manager.all()
            if campaign.get("status") == "active"
        ]

    def run_cycle(
        self,
        margin_percent=40,
        budget=10,
        channel="facebook_ads",
        tracking_prefix="HER"
    ):
        steps = []

        if not self.active_products():
            product_launch = self.launch_pipeline.launch_best_product(
                margin_percent
            )

            steps.append({
                "step": "launch_best_product",
                "result": product_launch
            })
        else:
            steps.append({
                "step": "launch_best_product",
                "result": {
                    "status": "skipped",
                    "message": "active product already exists"
                }
            })

        campaign_created = self.campaign_manager.create_for_best_active_product(
            budget,
            channel
        )

        steps.append({
            "step": "create_campaign",
            "result": campaign_created
        })

        if campaign_created.get("status") == "campaign_created":
            campaign = campaign_created.get("campaign", {})
            launched = self.campaign_manager.launch_campaign(campaign["id"])

            steps.append({
                "step": "launch_campaign",
                "result": launched
            })

        simulations = []

        for campaign in self.active_campaigns():
            simulations.append(
                self.campaign_manager.simulate_performance(
                    campaign["id"]
                )
            )

        steps.append({
            "step": "simulate_campaigns",
            "result": simulations
        })

        optimization = self.campaign_manager.optimize_campaigns()

        steps.append({
            "step": "optimize_campaigns",
            "result": optimization
        })

        fulfillment = self.order_manager.auto_fulfill_pending(
            tracking_prefix
        )

        steps.append({
            "step": "auto_fulfill_orders",
            "result": fulfillment
        })

        sales_report = self.sales_analytics.profit_report()
        campaign_report = self.campaign_manager.campaign_report()

        cycle = {
            "status": "store_autopilot_cycle_finished",
            "created_at": datetime.now().isoformat(),
            "settings": {
                "margin_percent": margin_percent,
                "budget": budget,
                "channel": channel,
                "tracking_prefix": tracking_prefix
            },
            "steps": steps,
            "sales_report": sales_report,
            "campaign_report": campaign_report
        }

        history = self.memory.get("store_autopilot_history", [])
        history.append(cycle)
        self.memory.set("store_autopilot_history", history)

        return cycle

    def history(self):
        return self.memory.get("store_autopilot_history", [])
