from datetime import datetime


class CampaignManager:

    def __init__(self, store, sales_analytics, memory, logger=None):
        self.store = store
        self.sales_analytics = sales_analytics
        self.memory = memory
        self.logger = logger

    def all(self):
        return self.memory.get("campaigns", [])

    def get_campaign(self, campaign_id):
        for campaign in self.all():
            if campaign["id"] == int(campaign_id):
                return campaign

        return None

    def get_product(self, product_id):
        for product in self.store.products():
            if product["id"] == int(product_id):
                return product

        return None

    def active_products(self):
        return [
            product for product in self.store.products()
            if product.get("published") is True
            or product.get("status") == "active"
        ]

    def create_campaign(
        self,
        product_id,
        budget=10,
        channel="facebook_ads"
    ):
        product = self.get_product(product_id)

        if not product:
            return {
                "status": "error",
                "message": "product not found"
            }

        title = product.get("title", "Produto")
        price = product.get("price", 0)
        category = product.get("category") or "geral"

        campaign = {
            "id": len(self.all()) + 1,
            "created_at": datetime.now().isoformat(),
            "product_id": product["id"],
            "product_title": title,
            "channel": channel,
            "budget": float(budget or 10),
            "status": "draft",
            "objective": "sales",
            "audience": self.build_audience(category),
            "ad_copy": self.build_ad_copy(title, price),
            "creative_brief": self.build_creative_brief(title, category),
            "metrics": {
                "impressions": 0,
                "clicks": 0,
                "orders": 0,
                "revenue": 0,
                "profit": 0,
                "spend": 0,
                "ctr": 0,
                "conversion_rate": 0,
                "cpc": 0,
                "roas": 0
            },
            "optimizer": {
                "last_action": "none",
                "last_reason": None,
                "last_checked_at": None
            }
        }

        campaigns = self.all()
        campaigns.append(campaign)
        self.memory.set("campaigns", campaigns)

        return {
            "status": "campaign_created",
            "campaign": campaign
        }

    def create_for_best_active_product(self, budget=10, channel="facebook_ads"):
        products = self.active_products()

        if not products:
            return {
                "status": "error",
                "message": "no active products available"
            }

        best = products[0]

        return self.create_campaign(
            best["id"],
            budget,
            channel
        )

    def update_campaign(self, campaign_id, key, value):
        campaigns = self.all()

        for campaign in campaigns:
            if campaign["id"] == int(campaign_id):
                campaign[key] = value
                self.memory.set("campaigns", campaigns)

                return {
                    "status": "campaign_updated",
                    "campaign": campaign
                }

        return {
            "status": "error",
            "message": "campaign not found"
        }

    def launch_campaign(self, campaign_id):
        campaigns = self.all()

        for campaign in campaigns:
            if campaign["id"] == int(campaign_id):
                campaign["status"] = "active"
                campaign["launched_at"] = datetime.now().isoformat()
                self.memory.set("campaigns", campaigns)

                return {
                    "status": "campaign_launched",
                    "campaign": campaign
                }

        return {
            "status": "error",
            "message": "campaign not found"
        }

    def pause_campaign(self, campaign_id):
        campaigns = self.all()

        for campaign in campaigns:
            if campaign["id"] == int(campaign_id):
                campaign["status"] = "paused"
                campaign["paused_at"] = datetime.now().isoformat()
                self.memory.set("campaigns", campaigns)

                return {
                    "status": "campaign_paused",
                    "campaign": campaign
                }

        return {
            "status": "error",
            "message": "campaign not found"
        }

    def update_metrics(
        self,
        campaign_id,
        impressions=0,
        clicks=0,
        orders=0,
        revenue=0,
        profit=0,
        spend=0
    ):
        campaigns = self.all()

        for campaign in campaigns:
            if campaign["id"] == int(campaign_id):
                metrics = campaign.get("metrics", {})

                metrics["impressions"] = int(impressions or 0)
                metrics["clicks"] = int(clicks or 0)
                metrics["orders"] = int(orders or 0)
                metrics["revenue"] = float(revenue or 0)
                metrics["profit"] = float(profit or 0)
                metrics["spend"] = float(spend or 0)

                campaign["metrics"] = self.calculate_metrics(metrics)
                campaign["metrics_updated_at"] = datetime.now().isoformat()

                self.memory.set("campaigns", campaigns)

                return {
                    "status": "campaign_metrics_updated",
                    "campaign": campaign
                }

        return {
            "status": "error",
            "message": "campaign not found"
        }

    def calculate_metrics(self, metrics):
        impressions = int(metrics.get("impressions") or 0)
        clicks = int(metrics.get("clicks") or 0)
        orders = int(metrics.get("orders") or 0)
        revenue = float(metrics.get("revenue") or 0)
        spend = float(metrics.get("spend") or 0)

        ctr = 0
        conversion_rate = 0
        cpc = 0
        roas = 0

        if impressions > 0:
            ctr = (clicks / impressions) * 100

        if clicks > 0:
            conversion_rate = (orders / clicks) * 100

        if clicks > 0:
            cpc = spend / clicks

        if spend > 0:
            roas = revenue / spend

        metrics["ctr"] = round(ctr, 2)
        metrics["conversion_rate"] = round(conversion_rate, 2)
        metrics["cpc"] = round(cpc, 2)
        metrics["roas"] = round(roas, 2)

        return metrics

    def simulate_performance(self, campaign_id):
        campaign = self.get_campaign(campaign_id)

        if not campaign:
            return {
                "status": "error",
                "message": "campaign not found"
            }

        budget = float(campaign.get("budget") or 10)

        impressions = int(budget * 120)
        clicks = int(impressions * 0.025)
        orders = int(clicks * 0.08)

        product = self.get_product(campaign.get("product_id"))
        price = float(product.get("price") or 20) if product else 20
        cost = float(product.get("cost") or 8) if product else 8

        revenue = orders * price
        profit = revenue - (orders * cost) - budget
        spend = budget

        return self.update_metrics(
            campaign_id,
            impressions,
            clicks,
            orders,
            revenue,
            profit,
            spend
        )

    def optimize_campaigns(self):
        campaigns = self.all()
        results = []

        for campaign in campaigns:
            if campaign.get("status") != "active":
                continue

            metrics = campaign.get("metrics", {})
            roas = float(metrics.get("roas") or 0)
            clicks = int(metrics.get("clicks") or 0)
            orders = int(metrics.get("orders") or 0)
            profit = float(metrics.get("profit") or 0)

            action = "keep_testing"
            reason = "insufficient_data"

            if clicks >= 20 and orders == 0:
                campaign["status"] = "paused"
                action = "pause"
                reason = "clicks_without_orders"

            elif roas >= 2 and profit > 0:
                campaign["budget"] = round(float(campaign.get("budget") or 10) * 1.2, 2)
                action = "scale_budget"
                reason = "profitable_campaign"

            elif roas < 1 and clicks >= 20:
                campaign["status"] = "paused"
                action = "pause"
                reason = "low_roas"

            elif roas >= 1:
                action = "keep_running"
                reason = "acceptable_performance"

            campaign["optimizer"] = {
                "last_action": action,
                "last_reason": reason,
                "last_checked_at": datetime.now().isoformat()
            }

            results.append({
                "campaign_id": campaign["id"],
                "product_title": campaign.get("product_title"),
                "action": action,
                "reason": reason,
                "status": campaign.get("status"),
                "budget": campaign.get("budget"),
                "metrics": campaign.get("metrics")
            })

        self.memory.set("campaigns", campaigns)

        optimization = {
            "status": "campaigns_optimized",
            "checked_campaigns": len(results),
            "results": results,
            "created_at": datetime.now().isoformat()
        }

        history = self.memory.get("campaign_optimization_history", [])
        history.append(optimization)
        self.memory.set("campaign_optimization_history", history)

        return optimization

    def performance_report(self):
        campaigns = self.all()

        ranked = sorted(
            campaigns,
            key=lambda campaign: float(campaign.get("metrics", {}).get("roas") or 0),
            reverse=True
        )

        report = {
            "status": "campaign_performance_report",
            "campaigns": ranked,
            "last_optimization": self.memory.get("campaign_optimization_history", [])[-1:]
        }

        self.memory.set("last_campaign_performance_report", report)

        return report

    def build_audience(self, category):
        return {
            "location": "Portugal",
            "age": "18-45",
            "interests": [
                category,
                "compras online",
                "gadgets",
                "promoções",
                "tecnologia"
            ],
            "platforms": [
                "facebook",
                "instagram"
            ]
        }

    def build_ad_copy(self, title, price):
        return {
            "headline": f"{title} em promoção",
            "primary_text": f"Descobre o {title}. Produto selecionado, preço competitivo e ideal para compra online.",
            "description": f"Disponível por apenas {price}. Aproveita antes que esgote.",
            "call_to_action": "Comprar agora"
        }

    def build_creative_brief(self, title, category):
        return {
            "format": "square_image_or_short_video",
            "style": "moderno, limpo, direto e com foco no produto",
            "message": f"Mostrar o produto {title} como uma solução útil para o dia a dia.",
            "visual_elements": [
                "produto em destaque",
                "benefício principal em texto curto",
                "preço visível",
                "botão Comprar Agora"
            ],
            "category": category
        }

    def campaign_report(self):
        campaigns = self.all()

        active = len([
            campaign for campaign in campaigns
            if campaign.get("status") == "active"
        ])

        draft = len([
            campaign for campaign in campaigns
            if campaign.get("status") == "draft"
        ])

        paused = len([
            campaign for campaign in campaigns
            if campaign.get("status") == "paused"
        ])

        total_budget = sum(
            float(campaign.get("budget") or 0)
            for campaign in campaigns
        )

        report = {
            "status": "campaign_report",
            "total_campaigns": len(campaigns),
            "active_campaigns": active,
            "draft_campaigns": draft,
            "paused_campaigns": paused,
            "total_budget": round(total_budget, 2),
            "campaigns": campaigns
        }

        self.memory.set("last_campaign_report", report)

        return report
