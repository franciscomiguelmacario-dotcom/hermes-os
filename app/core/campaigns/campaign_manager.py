from datetime import datetime


class CampaignManager:

    def __init__(self, store, sales_analytics, memory, logger=None):
        self.store = store
        self.sales_analytics = sales_analytics
        self.memory = memory
        self.logger = logger

    def all(self):
        return self.memory.get("campaigns", [])

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
                "profit": 0
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
