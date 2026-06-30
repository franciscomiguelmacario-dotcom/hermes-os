from datetime import datetime


class DropshippingAutopilot:

    def __init__(
        self,
        launch_pipeline,
        campaign_manager,
        order_manager,
        sales_analytics,
        memory,
        logger=None,
        notifications=None,
        customer_support=None,
        fulfillment_pipeline=None
    ):
        self.launch_pipeline = launch_pipeline
        self.campaign_manager = campaign_manager
        self.order_manager = order_manager
        self.sales_analytics = sales_analytics
        self.memory = memory
        self.logger = logger
        self.notifications = notifications
        self.customer_support = customer_support
        self.fulfillment_pipeline = fulfillment_pipeline

    def config(self):
        default = {
            "enabled": True,
            "max_active_campaigns": 3,
            "max_daily_budget": 50,
            "max_products": 20,
            "allow_product_launch": True,
            "allow_campaign_creation": True,
            "allow_campaign_launch": True,
            "allow_campaign_simulation": True,
            "allow_campaign_optimization": True,
            "allow_supplier_submission": True,
            "allow_auto_fulfillment": True,
            "allow_support_auto_reply": True,
            "allow_send_notifications": True
        }

        saved = self.memory.get("store_autopilot_config", {})

        if not isinstance(saved, dict):
            saved = {}

        config = {**default, **saved}
        self.memory.set("store_autopilot_config", config)

        return config

    def set_config_value(self, key, value):
        config = self.config()

        if key not in config:
            return {
                "status": "error",
                "message": "invalid config key",
                "valid_keys": list(config.keys())
            }

        if str(value).lower() in ["true", "yes", "1"]:
            value = True
        elif str(value).lower() in ["false", "no", "0"]:
            value = False
        else:
            try:
                if "." in str(value):
                    value = float(value)
                else:
                    value = int(value)
            except Exception:
                pass

        config[key] = value
        self.memory.set("store_autopilot_config", config)

        return {
            "status": "autopilot_config_updated",
            "config": config
        }

    def active_products(self):
        return self.campaign_manager.active_products()

    def active_campaigns(self):
        return [
            campaign for campaign in self.campaign_manager.all()
            if campaign.get("status") == "active"
        ]

    def total_active_budget(self):
        return sum(
            float(campaign.get("budget") or 0)
            for campaign in self.active_campaigns()
        )

    def safety_check(self, requested_budget=0):
        config = self.config()

        if not config.get("enabled"):
            return {
                "allowed": False,
                "reason": "autopilot_disabled",
                "config": config
            }

        active_campaigns = len(self.active_campaigns())
        max_active_campaigns = int(config.get("max_active_campaigns") or 0)

        if active_campaigns >= max_active_campaigns:
            return {
                "allowed": False,
                "reason": "max_active_campaigns_reached",
                "active_campaigns": active_campaigns,
                "max_active_campaigns": max_active_campaigns
            }

        total_budget = self.total_active_budget() + float(requested_budget or 0)
        max_daily_budget = float(config.get("max_daily_budget") or 0)

        if total_budget > max_daily_budget:
            return {
                "allowed": False,
                "reason": "max_daily_budget_exceeded",
                "total_budget_after_request": round(total_budget, 2),
                "max_daily_budget": max_daily_budget
            }

        products_count = len(self.active_products())
        max_products = int(config.get("max_products") or 0)

        if products_count >= max_products:
            return {
                "allowed": False,
                "reason": "max_products_reached",
                "products_count": products_count,
                "max_products": max_products
            }

        return {
            "allowed": True,
            "reason": "safe_to_run",
            "active_campaigns": active_campaigns,
            "active_budget": round(self.total_active_budget(), 2),
            "products_count": products_count
        }

    def run_cycle(
        self,
        margin_percent=40,
        budget=10,
        channel="facebook_ads",
        tracking_prefix="HER"
    ):
        config = self.config()
        steps = []

        safety = self.safety_check(budget)

        steps.append({
            "step": "safety_check",
            "result": safety
        })

        if not safety.get("allowed"):
            cycle = {
                "status": "store_autopilot_blocked",
                "created_at": datetime.now().isoformat(),
                "reason": safety.get("reason"),
                "settings": {
                    "margin_percent": margin_percent,
                    "budget": budget,
                    "channel": channel,
                    "tracking_prefix": tracking_prefix
                },
                "config": config,
                "steps": steps
            }

            self.save_cycle(cycle)
            return cycle

        if config.get("allow_product_launch") and not self.active_products():
            product_launch = self.launch_pipeline.launch_best_product(
                margin_percent
            )
        else:
            product_launch = {
                "status": "skipped",
                "message": "product launch disabled or active product already exists"
            }

        steps.append({
            "step": "launch_best_product",
            "result": product_launch
        })

        if config.get("allow_campaign_creation"):
            campaign_created = self.campaign_manager.create_for_best_active_product(
                budget,
                channel
            )
        else:
            campaign_created = {
                "status": "skipped",
                "message": "campaign creation disabled"
            }

        steps.append({
            "step": "create_campaign",
            "result": campaign_created
        })

        if (
            config.get("allow_campaign_launch")
            and campaign_created.get("status") == "campaign_created"
        ):
            campaign = campaign_created.get("campaign", {})
            launched = self.campaign_manager.launch_campaign(campaign["id"])
        else:
            launched = {
                "status": "skipped",
                "message": "campaign launch disabled or no campaign created"
            }

        steps.append({
            "step": "launch_campaign",
            "result": launched
        })

        simulations = []

        if config.get("allow_campaign_simulation"):
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

        if config.get("allow_campaign_optimization"):
            optimization = self.campaign_manager.optimize_campaigns()
            self.create_campaign_notifications(optimization)
        else:
            optimization = {
                "status": "skipped",
                "message": "campaign optimization disabled"
            }

        steps.append({
            "step": "optimize_campaigns",
            "result": optimization
        })

        if (
            config.get("allow_supplier_submission")
            and config.get("allow_auto_fulfillment")
            and self.fulfillment_pipeline
        ):
            supplier_submission = self.fulfillment_pipeline.submit_pending_orders()
        else:
            supplier_submission = {
                "status": "skipped",
                "message": "supplier submission disabled or fulfillment pipeline unavailable"
            }

        steps.append({
            "step": "submit_pending_orders_to_supplier",
            "result": supplier_submission
        })

        if (
            config.get("allow_support_auto_reply")
            and self.customer_support
        ):
            support = self.customer_support.auto_reply_all()
        else:
            support = {
                "status": "skipped",
                "message": "support auto reply disabled or unavailable"
            }

        steps.append({
            "step": "auto_reply_support",
            "result": support
        })

        if (
            config.get("allow_send_notifications")
            and self.notifications
        ):
            notification_send = self.notifications.send_pending()
        else:
            notification_send = {
                "status": "skipped",
                "message": "send notifications disabled or unavailable"
            }

        steps.append({
            "step": "send_notifications",
            "result": notification_send
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
            "config": config,
            "steps": steps,
            "sales_report": sales_report,
            "campaign_report": campaign_report
        }

        self.save_cycle(cycle)

        return cycle

    def create_campaign_notifications(self, optimization):
        if not self.notifications:
            return

        for item in optimization.get("results", []):
            campaign = self.campaign_manager.get_campaign(
                item.get("campaign_id")
            )

            if campaign:
                self.notifications.campaign_alert(
                    campaign,
                    item.get("action"),
                    item.get("reason")
                )

    def save_cycle(self, cycle):
        history = self.memory.get("store_autopilot_history", [])
        history.append(cycle)
        self.memory.set("store_autopilot_history", history)

    def history(self):
        return self.memory.get("store_autopilot_history", [])
