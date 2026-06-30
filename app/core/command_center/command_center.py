import unicodedata


class CommandCenter:

    def __init__(self, brain, logger=None):
        self.brain = brain
        self.logger = logger

    def normalize(self, text):
        text = text.lower().strip()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))

        remove_words = [
            "jarvis",
            "hermes",
            "por favor",
            "faz favor",
            "ok",
            "olha"
        ]

        for word in remove_words:
            text = text.replace(word, "")

        return " ".join(text.split())

    def has_any(self, text, words):
        return any(word in text for word in words)

    def handle(self, text):
        original = text.strip()
        cmd = self.normalize(original)

        self.save_voice_debug(original, cmd)

        if not cmd:
            return {
                "status": "error",
                "message": "empty command"
            }

        if self.has_any(cmd, ["ajuda", "help", "comandos", "o que podes fazer"]):
            return self.help()

        if self.has_any(cmd, ["estado", "saude", "sistema", "status", "health"]):
            return self.brain.health_check()

        if self.has_any(cmd, ["abre dashboard", "abrir dashboard", "dashboard", "painel"]):
            return {
                "status": "dashboard_available",
                "action": "python hermes.py dashboard",
                "url": "http://127.0.0.1:5000"
            }

        if self.has_any(cmd, ["perfil", "negocio", "business", "loja"]):
            if not self.has_any(cmd, ["criar", "cria", "tarefa", "task"]):
                return self.brain.business_profile()

        if self.has_any(cmd, ["proxima acao", "proxima ação", "next action", "o que faco", "o que faço"]):
            return self.brain.next_action()

        if self.has_any(cmd, [
            "autopilot cycle",
            "ciclo autopilot",
            "ciclo automatico",
            "ciclo automatico",
            "piloto automatico ciclo",
            "executa ciclo"
        ]):
            return self.brain.autopilot_cycle(5)

        if self.has_any(cmd, [
            "autopilot",
            "autopiloto",
            "piloto automatico",
            "piloto automatico",
            "executa automatico"
        ]):
            return self.brain.autopilot_once()

        if self.has_any(cmd, [
            "business cycle",
            "ciclo negocio",
            "ciclo do negocio",
            "ciclo da loja",
            "ciclo dropshipping"
        ]):
            return self.brain.run_business_cycle()

        if self.has_any(cmd, [
            "workflow dropshipping",
            "inicia dropshipping",
            "começar dropshipping",
            "comecar dropshipping",
            "executar dropshipping"
        ]):
            return self.brain.run_workflow("dropshipping")

        if self.has_any(cmd, ["relatorio", "relatório", "report", "resumo"]):
            return self.brain.report()

        if self.has_any(cmd, ["exportar obsidian", "export obsidian", "guardar obsidian", "enviar obsidian"]):
            return self.brain.export_obsidian_report()

        if self.has_any(cmd, ["backup", "copia seguranca", "cópia segurança"]):
            return self.brain.create_backup()

        if self.has_any(cmd, ["limpar tarefas", "apagar tarefas", "clear tasks", "limpa tarefas"]):
            return self.brain.clear_tasks()

        if self.has_any(cmd, ["mostrar tarefas", "mostra tarefas", "ver tarefas", "tarefas", "tasks"]):
            return self.brain.tasks.all()

        task_title = self.extract_task(original)
        if task_title:
            return self.brain.create_task(task_title)

        business_result = self.extract_business_value(original)
        if business_result:
            key, value = business_result
            return self.brain.set_business_value(key, value)

        return self.brain.chat(original)

    def extract_task(self, text):
        normalized = self.normalize(text)

        triggers = [
            "cria uma tarefa para",
            "criar uma tarefa para",
            "cria tarefa para",
            "criar tarefa para",
            "nova tarefa para",
            "adicionar tarefa para",
            "adiciona tarefa para",
            "mete tarefa para",
            "faz tarefa para",
            "cria tarefa",
            "criar tarefa",
            "nova tarefa",
            "adicionar tarefa",
            "adiciona tarefa",
            "mete tarefa",
            "faz tarefa"
        ]

        for trigger in triggers:
            index = normalized.find(trigger)

            if index >= 0:
                start = index + len(trigger)
                title = normalized[start:].strip(" :-,")

                if title:
                    return title

        if "produto vencedor" in normalized:
            return "pesquisar produto vencedor"

        if "campanha" in normalized or "anuncio" in normalized or "anuncio" in normalized:
            return "criar campanha ads para produto vencedor"

        if "fornecedor" in normalized:
            return "encontrar fornecedor com envio rapido"

        return None

    def extract_business_value(self, text):
        normalized = self.normalize(text)

        mapping = {
            "nome da loja": "store_name",
            "nome loja": "store_name",
            "store name": "store_name",
            "nicho": "niche",
            "niche": "niche",
            "orcamento": "budget",
            "orçamento": "budget",
            "budget": "budget",
            "moeda": "currency",
            "currency": "currency"
        }

        starters = [
            "definir",
            "define",
            "guardar",
            "guarda",
            "mudar",
            "muda",
            "set"
        ]

        for phrase, key in mapping.items():
            if phrase in normalized and self.has_any(normalized, starters):
                index = normalized.find(phrase)
                start = index + len(phrase)
                value = normalized[start:].strip(" :-,como")

                if value:
                    return key, value

        return None

    def save_voice_debug(self, original, normalized):
        history = self.brain.memory.get("voice_command_history", [])

        history.append({
            "original": original,
            "normalized": normalized
        })

        history = history[-20:]
        self.brain.memory.set("voice_command_history", history)

    def help(self):
        return {
            "commands": [
                "mostra o estado",
                "abre o dashboard",
                "mostra o perfil do negócio",
                "qual é a próxima ação",
                "executa autopilot",
                "executa autopilot cycle",
                "inicia workflow dropshipping",
                "cria tarefa pesquisar produto vencedor",
                "mostra tarefas",
                "limpa tarefas",
                "gerar relatório",
                "exportar obsidian",
                "fazer backup",
                "definir nome da loja Hermes Store",
                "definir nicho gadgets",
                "definir orçamento 100"
            ]
        }
