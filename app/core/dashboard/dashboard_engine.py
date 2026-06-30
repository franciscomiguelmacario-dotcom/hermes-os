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

    def mask_sensitive_config(self, config):
        if not isinstance(config, dict):
            return config

        masked = dict(config)

        for key in ["api_key", "api_secret", "access_token"]:
            value = masked.get(key)

            if value:
                masked[key] = "***configured***"
            else:
                masked[key] = ""

        return masked

    def latest_item(self, value):
        if isinstance(value, list) and value:
            return value[-1]

        return None

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

        store_api_config = self.safe("store_api_config", {})
        store_api_history = self.safe("store_api_history", [])

        supplier_api_config = self.safe("supplier_api_config", {})
        supplier_api_history = self.safe("supplier_api_history", [])

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
                "pending_support": self.count_list(pending_support),
                "store_api_events": self.count_list(store_api_history),
                "supplier_api_events": self.count_list(supplier_api_history)
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
            "store_api": {
                "config": self.mask_sensitive_config(store_api_config),
                "history_count": self.count_list(store_api_history),
                "latest_sync": self.latest_item(store_api_history)
            },
            "supplier_api": {
                "config": self.mask_sensitive_config(supplier_api_config),
                "history_count": self.count_list(supplier_api_history),
                "latest_sync": self.latest_item(supplier_api_history)
            },
            "autopilot": {
                "config": autopilot_config,
                "latest_cycle": self.latest_item(autopilot_history),
                "cycles_count": self.count_list(autopilot_history)
            },
            "alerts": self.alerts(
                pending_orders,
                pending_notifications,
                pending_support,
                active_campaigns,
                sales_summary,
                store_api_config,
                supplier_api_config
            ),
            "next_recommended_actions": self.next_actions(
                products,
                supplier_products,
                pending_orders,
                pending_notifications,
                pending_support,
                active_campaigns,
                store_api_config,
                supplier_api_config
            )
        }

        return dashboard

    def alerts(
        self,
        pending_orders,
        pending_notifications,
        pending_support,
        active_campaigns,
        sales_summary,
        store_api_config,
        supplier_api_config
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

        if not store_api_config.get("enabled"):
            alerts.append({
                "level": "info",
                "message": "Store API ainda não está ativa."
            })

        if store_api_config.get("dry_run"):
            alerts.append({
                "level": "warning",
                "message": "Store API está em modo dry-run. Nada será enviado para loja real."
            })

        if not supplier_api_config.get("enabled"):
            alerts.append({
                "level": "info",
                "message": "Supplier API ainda não está ativa."
            })

        if supplier_api_config.get("dry_run"):
            alerts.append({
                "level": "warning",
                "message": "Supplier API está em modo dry-run. Nenhuma encomenda real será enviada ao fornecedor."
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
        active_campaigns,
        store_api_config,
        supplier_api_config
    ):
        actions = []

        if not supplier_products:
            actions.append("Adicionar produtos de fornecedor.")

        if supplier_products and not products:
            actions.append("Lançar o melhor produto com launch-best-product 40.")

        if products and not active_campaigns:
            actions.append("Criar e lançar campanha para produto ativo.")

        if pending_orders:
            actions.append("Processar encomendas pendentes ou enviar para fornecedor.")

        if pending_support:
            actions.append("Responder tickets com auto-reply-support-all.")

        if pending_notifications:
            actions.append("Enviar notificações com send-notifications.")

        if not store_api_config.get("enabled"):
            actions.append("Configurar ligação à loja real no painel Store API.")

        if not supplier_api_config.get("enabled"):
            actions.append("Configurar ligação ao fornecedor no painel Supplier API.")

        if store_api_config.get("dry_run"):
            actions.append("Manter Store API em dry-run enquanto testas.")

        if supplier_api_config.get("dry_run"):
            actions.append("Manter Supplier API em dry-run enquanto testas.")

        if not actions:
            actions.append("Executar store-autopilot 40 | 10 | facebook_ads | HER.")

        return actions
