class BusinessProfile:

    def __init__(self, memory):
        self.memory = memory

    def get(self):
        return self.memory.get("business_profile", {
            "store_name": None,
            "niche": None,
            "budget": None,
            "currency": "EUR"
        })

    def set_value(self, key, value):
        profile = self.get()
        profile[key] = value
        self.memory.set("business_profile", profile)

        return {
            "status": "saved",
            "business_profile": profile
        }
