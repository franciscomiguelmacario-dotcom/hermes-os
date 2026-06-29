class Router:

    def __init__(self):
        self.routes = {}

    def register(self, command, callback):
        self.routes[command] = callback

    def execute(self, command):

        if command in self.routes:
            return self.routes[command]()

        print(f"Comando desconhecido: {command}")
