from datetime import datetime, timedelta
import unicodedata


class DropshippingBusinessToolkit:
    """Small deterministic playbook for dropshipping business agents."""

    def normalize(self, value):
        text = str(value or "").lower().strip()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        return " ".join(text.split())

    def safe_float(self, value, default=0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def safe_int(self, value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def product_name(self, product):
        if not isinstance(product, dict):
            return "Produto vencedor"

        return (
            product.get("name")
            or product.get("title")
            or product.get("product_title")
            or "Produto vencedor"
        )

    def product_category(self, product, niche=None):
        if not isinstance(product, dict):
            return niche or "geral"

        return product.get("category") or product.get("niche") or niche or "geral"

    def estimate_price(self, cost):
        cost = self.safe_float(cost)

        if cost <= 0:
            return 29.99

        return round(max(cost * 2.7, cost + 14.99), 2)

    def estimate_margin_percent(self, cost, price):
        cost = self.safe_float(cost)
        price = self.safe_float(price)

        if price <= 0:
            return 0

        return round(((price - cost) / price) * 100, 2)

    def seed_products(self, query=None, niche=None):
        niche = niche or query or "gadgets"
        clean_niche = self.normalize(niche) or "gadgets"

        products = [
            {
                "title": f"Kit viral para {clean_niche}",
                "cost": 11,
                "shipping_days": 8,
                "category": clean_niche,
                "source": "seed_research"
            },
            {
                "title": "Mini aspirador portatil sem fios",
                "cost": 12,
                "shipping_days": 7,
                "category": "casa_auto",
                "source": "seed_research"
            },
            {
                "title": "Luz LED inteligente com sensor",
                "cost": 8,
                "shipping_days": 8,
                "category": "casa_gadgets",
                "source": "seed_research"
            },
            {
                "title": "Garrafa termica inteligente",
                "cost": 14,
                "shipping_days": 10,
                "category": "fitness_lifestyle",
                "source": "seed_research"
            }
        ]

        return products

    def score_product(self, product, query=None, niche=None):
        title = self.normalize(self.product_name(product))
        category = self.normalize(self.product_category(product, niche))
        context = " ".join([title, category, self.normalize(query), self.normalize(niche)])

        cost = self.safe_float(product.get("cost") if isinstance(product, dict) else None)
        shipping_days = self.safe_int(
            product.get("shipping_days") if isinstance(product, dict) else None,
            99
        )

        demand_words = [
            "smart",
            "inteligente",
            "portable",
            "portatil",
            "mini",
            "wireless",
            "sem fios",
            "led",
            "fitness",
            "casa",
            "auto",
            "beleza",
            "pet",
            "cozinha"
        ]
        viral_words = [
            "viral",
            "mini",
            "smart",
            "inteligente",
            "led",
            "portatil",
            "sem fios",
            "sensor",
            "organizador",
            "kit"
        ]

        demand = 45
        demand += min(30, 10 * len([word for word in demand_words if word in context]))
        if category and category != "geral":
            demand += 10

        competition = 62
        if len(title.split()) >= 4:
            competition += 12
        if any(word in title for word in ["iphone", "airpods", "nike", "samsung"]):
            competition -= 25

        if cost <= 0:
            margin = 48
        elif cost <= 8:
            margin = 86
        elif cost <= 15:
            margin = 78
        elif cost <= 25:
            margin = 64
        else:
            margin = 42

        viral = 38 + min(42, 11 * len([word for word in viral_words if word in context]))

        if shipping_days <= 0 or shipping_days >= 99:
            shipping = 45
        elif shipping_days <= 7:
            shipping = 90
        elif shipping_days <= 10:
            shipping = 78
        elif shipping_days <= 15:
            shipping = 58
        else:
            shipping = 32

        scores = {
            "demand": min(demand, 95),
            "low_competition": max(min(competition, 90), 20),
            "margin": margin,
            "viral_potential": min(viral, 90),
            "shipping": shipping
        }

        total = round(
            scores["demand"] * 0.22
            + scores["low_competition"] * 0.18
            + scores["margin"] * 0.22
            + scores["viral_potential"] * 0.22
            + scores["shipping"] * 0.16
        )

        reasons = []
        risks = []

        if scores["demand"] >= 70:
            reasons.append("sinais de procura e interesse de compra")
        if scores["margin"] >= 70:
            reasons.append("margem potencial saudavel")
        if scores["viral_potential"] >= 65:
            reasons.append("bom potencial para criativos curtos")
        if scores["shipping"] >= 70:
            reasons.append("envio competitivo para validacao")

        if scores["low_competition"] < 55:
            risks.append("categoria pode estar saturada")
        if scores["shipping"] < 55:
            risks.append("prazo de envio pode reduzir conversao")
        if cost <= 0:
            risks.append("custo ainda precisa de validacao")

        if total >= 75:
            verdict = "winner_candidate"
        elif total >= 60:
            verdict = "test_candidate"
        elif total >= 45:
            verdict = "watch_candidate"
        else:
            verdict = "weak_candidate"

        return {
            "score": total,
            "scores": scores,
            "verdict": verdict,
            "reasons": reasons,
            "risks": risks
        }

    def build_campaign_inputs(self, product, query=None, niche=None):
        name = self.product_name(product)
        category = self.product_category(product, niche)

        return {
            "problem": f"Cliente procura uma solucao pratica em {category}.",
            "promise": f"{name} apresentado como uma melhoria simples para o dia a dia.",
            "audiences": [
                category,
                "compradores online",
                "pessoas interessadas em novidades uteis",
                "utilizadores que compram por demonstracao visual"
            ],
            "hooks": [
                f"Este {name} resolve um problema que muita gente ignora.",
                f"Testa isto antes de voltares a comprar produtos comuns de {category}.",
                f"O detalhe simples que torna {category} mais facil."
            ],
            "creative_notes": [
                "mostrar o produto em uso nos primeiros 3 segundos",
                "comparar antes/depois sem promessas exageradas",
                "fechar com preco, beneficio principal e chamada para acao"
            ],
            "query": query
        }

    def build_candidate(self, product, query=None, niche=None, source="research"):
        name = self.product_name(product)
        category = self.product_category(product, niche)
        cost = self.safe_float(product.get("cost") if isinstance(product, dict) else None)
        price = self.estimate_price(cost)
        score = self.score_product(product, query, niche)

        candidate = {
            "created_at": datetime.now().isoformat(),
            "name": name,
            "title": name,
            "niche": niche or category,
            "category": category,
            "source": product.get("source", source) if isinstance(product, dict) else source,
            "supplier_product_id": product.get("id") if isinstance(product, dict) else None,
            "supplier_url": product.get("supplier_url") if isinstance(product, dict) else None,
            "cost": cost,
            "estimated_price": price,
            "estimated_margin_percent": self.estimate_margin_percent(cost, price),
            "shipping_days": product.get("shipping_days") if isinstance(product, dict) else None,
            "score": score["score"],
            "scores": score["scores"],
            "verdict": score["verdict"],
            "reasons": score["reasons"],
            "risks": score["risks"],
            "campaign_ready": score["score"] >= 60,
            "campaign_inputs": self.build_campaign_inputs(product, query, niche)
        }

        return candidate

    def product_context(self, product):
        name = self.product_name(product)
        category = self.product_category(product)

        return {
            "id": product.get("id") if isinstance(product, dict) else None,
            "candidate_id": product.get("id") if isinstance(product, dict) else None,
            "supplier_product_id": product.get("supplier_product_id") if isinstance(product, dict) else None,
            "name": name,
            "title": name,
            "category": category,
            "price": (
                product.get("estimated_price")
                or product.get("price")
                or self.estimate_price(product.get("cost"))
            ) if isinstance(product, dict) else 29.99,
            "cost": product.get("cost") if isinstance(product, dict) else None,
            "score": product.get("score") if isinstance(product, dict) else None,
            "verdict": product.get("verdict") if isinstance(product, dict) else None
        }

    def build_marketing_plan(self, product, platform="multi"):
        context = self.product_context(product)
        name = context["name"]
        category = context["category"]
        platform = platform or "multi"

        platforms = ["Meta Ads", "TikTok Ads", "Google Ads"]
        platform_key = self.normalize(platform)

        if platform_key in ["meta", "meta ads", "facebook", "facebook ads", "instagram"]:
            platforms = ["Meta Ads"]
        elif platform_key in ["tiktok", "tiktok ads"]:
            platforms = ["TikTok Ads"]
        elif platform_key in ["google", "google ads", "search"]:
            platforms = ["Google Ads"]

        angles = [
            {
                "name": "problema-solucao",
                "copy": f"Mostra o problema diario em {category} e apresenta {name} como solucao simples."
            },
            {
                "name": "demonstracao-rapida",
                "copy": f"Video curto com {name} em uso real, beneficio visivel e chamada para acao."
            },
            {
                "name": "curiosidade",
                "copy": f"Hook de descoberta: porque tantos compradores estao a testar {name}."
            }
        ]

        headlines = [
            f"{name} para simplificar o dia",
            f"Descobre o {name}",
            f"Uma melhoria simples para {category}",
            f"{name}: util, visual e facil de testar"
        ]

        descriptions = [
            f"Produto selecionado para validar procura em {category}.",
            "Criativo curto, beneficio claro e oferta direta.",
            "Ideal para campanha de teste com baixo orcamento."
        ]

        return {
            "created_at": datetime.now().isoformat(),
            "status": "marketing_plan_created",
            "product": context,
            "platforms": platforms,
            "angles": angles,
            "headlines": headlines,
            "short_descriptions": descriptions,
            "primary_texts": [
                f"Transforma uma tarefa comum com {name}. Ve a demonstracao e decide em segundos.",
                f"Se gostas de solucoes praticas em {category}, este produto merece um teste.",
                f"Um produto simples, visual e pronto para validar com trafego pago controlado."
            ],
            "creative_briefs": [
                {
                    "format": "short_video",
                    "duration_seconds": 15,
                    "structure": [
                        "hook visual",
                        "demonstracao",
                        "beneficio",
                        "oferta",
                        "call_to_action"
                    ]
                },
                {
                    "format": "square_image",
                    "structure": [
                        "produto em destaque",
                        "beneficio principal",
                        "preco ou oferta",
                        "botao de compra"
                    ]
                }
            ],
            "test_plan": {
                "daily_budget": 10,
                "duration_days": 3,
                "success_metrics": ["CTR", "CPC", "CPA", "ROAS", "orders"],
                "stop_rules": [
                    "pausar se houver muitos cliques sem compras",
                    "pausar se CPC subir acima do limite definido",
                    "escalar apenas com ROAS positivo"
                ]
            },
            "future_campaigns": [
                {
                    "platform": platform_name,
                    "objective": "sales",
                    "status": "draft_ready"
                }
                for platform_name in platforms
            ]
        }

    def build_organic_plan(self, product, days=7):
        context = self.product_context(product)
        name = context["name"]
        category = context["category"]
        days = max(1, min(self.safe_int(days, 7), 30))
        start = datetime.now().date()

        post_ideas = [
            f"Antes/depois usando {name}",
            f"3 situacoes em que {name} ajuda em {category}",
            f"Teste honesto de 15 segundos com {name}",
            f"Erro comum em {category} e como resolver",
            f"Unboxing rapido e primeira impressao de {name}"
        ]

        short_videos = [
            {
                "hook": f"Nao compres mais nada de {category} sem ver isto.",
                "body": f"Mostrar {name} em uso real.",
                "cta": "Comenta para receber o link."
            },
            {
                "hook": "Isto parece simples, mas poupa tempo.",
                "body": f"Demonstrar uma transformacao clara com {name}.",
                "cta": "Guarda para veres depois."
            },
            {
                "hook": "Produto barato ou solucao util?",
                "body": f"Comparar expectativa vs realidade de {name}.",
                "cta": "Segue para mais testes."
            }
        ]

        calendar = []
        channels = ["TikTok", "Instagram Reels", "YouTube Shorts"]

        for index in range(days):
            calendar.append({
                "day": index + 1,
                "date": (start + timedelta(days=index)).isoformat(),
                "channel": channels[index % len(channels)],
                "idea": post_ideas[index % len(post_ideas)],
                "format": "short_video",
                "status": "planned"
            })

        return {
            "created_at": datetime.now().isoformat(),
            "status": "organic_plan_created",
            "product": context,
            "channels": channels + ["SEO Blog"],
            "content_pillars": [
                "demonstracao real",
                "problema e solucao",
                "prova visual",
                "comparacao antes/depois",
                "respostas a duvidas"
            ],
            "post_ideas": post_ideas,
            "short_video_ideas": short_videos,
            "calendar": calendar,
            "metrics_to_track": [
                "views",
                "watch_time",
                "saves",
                "comments",
                "profile_clicks",
                "link_clicks"
            ]
        }
