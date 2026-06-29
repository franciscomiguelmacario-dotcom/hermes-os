class DecisionEngine:

    def __init__(self, memory, tasks):
        self.memory = memory
        self.tasks = tasks

    def next_action(self):
        profile = self.memory.get("business_profile", {})
        pending = self.tasks.pending()

        if not profile.get("store_name"):
            return {
                "priority": "high",
                "action": "set-business store_name <nome_da_loja>",
                "reason": "nome da loja ainda não configurado"
            }

        if not profile.get("niche"):
            return {
                "priority": "high",
                "action": "set-business niche <nicho>",
                "reason": "nicho ainda não configurado"
            }

        if pending:
            return {
                "priority": "medium",
                "action": "tasks",
                "reason": f"existem {len(pending)} tarefas pendentes"
            }

        if not self.memory.get("last_product_research"):
            return {
                "priority": "high",
                "action": "task pesquisar produto vencedor",
                "reason": "ainda não existe pesquisa de produto"
            }

        if not self.memory.get("last_marketing_plan"):
            return {
                "priority": "medium",
                "action": "task criar campanha ads para produto vencedor",
                "reason": "ainda não existe plano de marketing"
            }

        return {
            "priority": "normal",
            "action": "workflow dropshipping",
            "reason": "sistema pronto para novo ciclo de otimização"
        }
