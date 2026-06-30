from decimal import Decimal, ROUND_UP


class PricingEngine:

    def __init__(self, memory, logger=None):
        self.memory = memory
        self.logger = logger

    def config(self):
        return self.memory.get("pricing_config", {
            "target_margin_percent": "35",
            "platform_fee_percent": "3",
            "payment_fee_percent": "2",
            "fixed_fee": "0.35",
            "rounding": "0.99",
            "currency": "EUR"
        })

    def set_value(self, key, value):
        config = self.config()
        config[key] = str(value)
        self.memory.set("pricing_config", config)

        return {
            "status": "pricing_config_saved",
            "pricing_config": config
        }

    def money(self, value):
        return Decimal(str(value or "0")).quantize(Decimal("0.01"))

    def calculate(self, cost, shipping=0, margin_percent=None):
        config = self.config()

        cost = self.money(cost)
        shipping = self.money(shipping)

        target_margin = Decimal(str(
            margin_percent or config.get("target_margin_percent", "35")
        )) / Decimal("100")

        platform_fee = Decimal(str(config.get("platform_fee_percent", "3"))) / Decimal("100")
        payment_fee = Decimal(str(config.get("payment_fee_percent", "2"))) / Decimal("100")
        fixed_fee = self.money(config.get("fixed_fee", "0.35"))

        total_cost = cost + shipping
        total_fee_percent = platform_fee + payment_fee

        denominator = Decimal("1") - target_margin - total_fee_percent

        if denominator <= 0:
            return {
                "status": "error",
                "message": "invalid margin or fees"
            }

        raw_price = (total_cost + fixed_fee) / denominator
        recommended_price = self.round_price(raw_price)

        estimated_fees = (recommended_price * total_fee_percent) + fixed_fee
        estimated_profit = recommended_price - total_cost - estimated_fees
        estimated_margin = (estimated_profit / recommended_price) * Decimal("100")

        return {
            "status": "price_calculated",
            "currency": config.get("currency", "EUR"),
            "cost": float(cost),
            "shipping": float(shipping),
            "total_cost": float(total_cost),
            "recommended_price": float(recommended_price),
            "estimated_fees": float(estimated_fees.quantize(Decimal("0.01"))),
            "estimated_profit": float(estimated_profit.quantize(Decimal("0.01"))),
            "estimated_margin_percent": float(estimated_margin.quantize(Decimal("0.01"))),
            "target_margin_percent": float(target_margin * Decimal("100"))
        }

    def round_price(self, price):
        price = Decimal(price).quantize(Decimal("1"), rounding=ROUND_UP)

        rounded = price - Decimal("0.01")

        if rounded <= 0:
            rounded = Decimal("0.99")

        return rounded.quantize(Decimal("0.01"))
