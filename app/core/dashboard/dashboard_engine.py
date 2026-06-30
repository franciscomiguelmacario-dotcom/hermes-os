
from datetime import datetime


class DashboardEngine:

    def __init__(self, brain):
        self.brain = brain

    def safe(self, method_name, default=None):
        try:
            method = getattr(self.brain, method_name, None)

            if not method:
                return default

            return method()
        except Exception as error:
            return {
                "status": "error",
                "method": method_name,
                "message": str(error)
            }

    def count_list(self, value):
        if isinstance(value, list):
            return len(value)

        return 0

    def data(self):
        products = self.safe("store_products", [])
        supplier_products = self.safe("supplier_products", [])
        orders = self.safe("orders_all", [])
        pending_orders = self.safe("pending_orders", [])
        campaigns = self.safe("campaigns_all", [])
        notifications = self.safe("notifications_all", [])
        pending_notifications = self.safe("pending_notifications", [])
        support_tickets = self.safe("support_tickets", [])
        pending_support = self.safe("pending_support_tickets", [])

        sales_summary = self.safe("sales_summary", {})
        profit_report = self.safe("profit_report", {})
        campaign_report = self.safe("campaign_report", {})
        campaign_performance = self.safe("campaign_performance", {})
        autopilot_config = self.safe("store_autopilot_config", {})
        autopilot_history = self.safe("store_autopilot_history", [])

        active_products = [
            product for product in products
            if product.get("status") == "active"
            or product.get("published") is True
        ]

        active_campaigns = [
            campaign for campaign in campaigns
            if campaign.get("status") == "active"
        ]

        paused_campaigns = [
            campaign for campaign in campaigns
            if campaign.get("status") == "paused"
        ]

        fulfilled_orders = [
            order for order in orders
            if order.get("fulfillment_status") == "fulfilled"
        ]

        latest_cycle = None
        if isinstance(autopilot_history, list) and autopilot_history:
            latest_cycle = autopilot_history[-1]

        dashboard = {
            "status": "dashboard_ready",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "products": self.count_list(products),
                "active_products": self.count_list(active_products),
                "supplier_products": self.count_list(supplier_products),
                "orders": self.count_list(orders),
                "pending_orders": self.count_list(pending_orders),
                "fulfilled_orders": self.count_list(fulfilled_orders),
                "campaigns": self.count_list(campaigns),
                "active_campaigns": self.count_list(active_campaigns),
                "paused_campaigns": self.count_list(paused_campaigns),
                "notifications": self.count_list(notifications),
                "pending_notifications": self.count_list(pending_notifications),
                "support_tickets": self.count_list(support_tickets),
                "pending_support": self.count_list(pending_support)
            },
            "money": {
                "revenue": sales_summary.get("revenue", 0),
                "costs": sales_summary.get("costs", 0),
                "profit": sales_summary.get("profit", 0),
                "average_order_value": sales_summary.get("average_order_value", 0)
            },
            "sales_summary": sales_summary,
            "profit_report": profit_report,
            "campaign_report": campaign_report,
            "campaign_performance": campaign_performance,
            "autopilot": {
                "config": autopilot_config,
                "latest_cycle": latest_cycle,
                "cycles_count": self.count_list(autopilot_history)
            },
            "alerts": self.alerts(
                pending_orders,
                pending_notifications,
                pending_support,
                active_campaigns,
                sales_summary
            ),
            "next_recommended_actions": self.next_actions(
                products,
                supplier_products,
                pending_orders,
                pending_notifications,
                pending_support,
                active_campaigns
            )
        }

        return dashboard

    def alerts(
        self,
        pending_orders,
        pending_notifications,
        pending_support,
        active_campaigns,
        sales_summary
    ):
        alerts = []

        if pending_orders:
            alerts.append({
                "level": "warning",
                "message": f"{len(pending_orders)} encomenda(s) pendente(s)."
            })

        if pending_notifications:
            alerts.append({
                "level": "info",
                "message": f"{len(pending_notifications)} notificação(ões) por enviar."
            })

        if pending_support:
            alerts.append({
                "level": "warning",
                "message": f"{len(pending_support)} ticket(s) de suporte aberto(s)."
            })

        if not active_campaigns:
            alerts.append({
                "level": "info",
                "message": "Não há campanhas ativas."
            })

        profit = float(sales_summary.get("profit") or 0)

        if profit < 0:
            alerts.append({
                "level": "danger",
                "message": "Lucro estimado negativo."
            })

        if not alerts:
            alerts.append({
                "level": "ok",
                "message": "Sistema operacional sem alertas críticos."
            })

        return alerts

    def next_actions(
        self,
        products,
        supplier_products,
        pending_orders,
        pending_notifications,
        pending_support,
        active_campaigns
    ):
        actions = []

        if not supplier_products:
            actions.append("Adicionar produtos de fornecedor.")

        if supplier_products and not products:
            actions.append("Lançar o melhor produto com launch-best-product 40.")

        if products and not active_campaigns:
            actions.append("Criar e lançar campanha para produto ativo.")

        if pending_orders:
            actions.append("Processar encomendas pendentes com auto-fulfill-orders HER.")

        if pending_support:
            actions.append("Responder tickets com auto-reply-support-all.")

        if pending_notifications:
            actions.append("Enviar notificações com send-notifications.")

        if not actions:
            actions.append("Executar store-autopilot 40 | 10 | facebook_ads | HER.")

        return actions
