class WorkflowEngine:

    def __init__(self, task_queue, logger):
        self.task_queue = task_queue
        self.logger = logger

    def list(self):
        return [
            "dropshipping"
        ]

    def run(self, name):
        name = name.lower().strip()

        if name == "dropshipping":
            return self._dropshipping_workflow()

        return {
            "status": "error",
            "message": f"workflow not found: {name}"
        }

    def _dropshipping_workflow(self):
        tasks = [
            "pesquisar produto vencedor",
            "encontrar fornecedor com envio rapido",
            "melhorar design da loja para vender mais",
            "criar campanha ads para produto vencedor",
            "criar plano de trafego organico para produto vencedor",
            "automatizar loja dropshipping",
            "analisar metricas de vendas e lucro",
            "responder mensagem cliente sobre encomenda atrasada",
            "processar pedido e atualizar tracking"
        ]

        created = []

        for title in tasks:
            created.append(self.task_queue.add(title))

        self.logger.info("[workflow] dropshipping workflow created")

        return {
            "status": "created",
            "workflow": "dropshipping",
            "tasks": created
        }
