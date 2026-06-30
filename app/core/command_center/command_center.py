import unicodedata


class CommandCenter:

    def __init__(self, brain, logger=None):
        self.brain = brain
        self.logger = logger

    def normalize(self, text):
        text = text.lower().strip()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        return text

    def handle(self, text):
        original = text.strip()
        cmd = self.normalize(original)

        if not cmd:
            return {
                "status": "error",
                "message": "empty command"
            }

        if cmd in ["ajuda", "help", "comandos"]:
            return self.help()

        if "estado" in cmd or "saude" in cmd or "health" in cmd:
            return self.brain.health_check()

        if "dashboard" in cmd:
            return {
                "status": "dashboard_available",
                "action": "python hermes.py dashboard",
                "url": "http://127.0.0.1:5000"
            }

        if "perfil" in cmd or "negocio" in cmd or "business" in cmd:
            return self.brain.business_profile()

        if "proxima acao" in cmd or "next action" in cmd:
            return self.brain.next_action()

        if "autopilot cycle" in cmd or "ciclo autopilot" in cmd:
            return self.brain.autopilot_cycle(5)

        if "autopilot" in cmd or "autopiloto" in cmd:
            return self.brain.autopilot_once()

        if "business cycle" in cmd or "ciclo negocio" in cmd or "ciclo do negocio" in cmd:
            return self.brain.run_business_cycle()

        if "workflow dropshipping" in cmd or "inicia dropshipping" in cmd:
            return self.brain.run_workflow("dropshipping")

        if "relatorio" in cmd or "report" in cmd:
            return self.brain.report()

        if "exportar obsidian" in cmd or "export obsidian" in cmd:
            return self.brain.export_obsidian_report()

        if "backup" in cmd:
            return self.brain.create_backup()

        if "limpar tarefas" in cmd or "clear tasks" in cmd:
            return self.brain.clear_tasks()

        if "tarefas" in cmd or "tasks" in cmd:
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
            "cria tarefa",
            "criar tarefa",
            "nova tarefa",
            "adicionar tarefa"
        ]

        for trigger in triggers:
            index = normalized.find(trigger)

            if index >= 0:
                start = index + len(trigger)
                title = text[start:].strip(" :-,")

                if title:
                    return title

        return None

    def extract_business_value(self, text):
        normalized = self.normalize(text)

        mapping = {
            "nome da loja": "store_name",
            "store name": "store_name",
            "nicho": "niche",
            "niche": "niche",
            "orcamento": "budget",
            "budget": "budget",
            "moeda": "currency",
            "currency": "currency"
        }

        for phrase, key in mapping.items():
            if phrase in normalized:
                index = normalized.find(phrase)
                start = index + len(phrase)
                value = text[start:].strip(" :-,")

                if value:
                    return key, value

        return None

    def help(self):
        return {
            "commands": [
                "jarvis mostra o estado",
                "jarvis abre o dashboard",
                "jarvis mostra o perfil do negócio",
                "jarvis qual é a próxima ação",
                "jarvis executa autopilot",
                "jarvis executa autopilot cycle",
                "jarvis inicia workflow dropshipping",
                "jarvis cria tarefa pesquisar produto vencedor",
                "jarvis mostra tarefas",
                "jarvis limpar tarefas",
                "jarvis gerar relatório",
                "jarvis exportar obsidian",
                "jarvis fazer backup",
                "jarvis definir nome da loja Hermes Store",
                "jarvis definir nicho gadgets",
                "jarvis definir orçamento 100",
                "jarvis o que achas do negócio?"
            ]
        }
