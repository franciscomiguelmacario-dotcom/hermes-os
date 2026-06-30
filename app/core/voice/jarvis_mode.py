class JarvisMode:

    def __init__(self, brain, logger=None):
        self.brain = brain
        self.logger = logger
        self.running = False

    def start(self, cycles=10, seconds=7):
        self.running = True
        history = []

        self.brain.speak("Hermes modo Jarvis ativado.")

        for _ in range(cycles):
            if not self.running:
                break

            if self.logger:
                self.logger.info("A ouvir...")

            heard = self.brain.listen_once(seconds)

            if self.logger:
                self.logger.info({
                    "heard": heard
                })

            if heard.get("status") != "ok":
                history.append(heard)
                continue

            text = heard.get("text", "").strip()

            if not text:
                continue

            self.brain.memory.set("last_voice_command", text)

            if self.should_stop(text):
                self.brain.speak("Modo Jarvis terminado.")
                self.running = False

                result = {
                    "status": "jarvis_mode_stopped",
                    "heard": text
                }

                history.append(result)
                break

            result = self.brain.handle_command_voice(text)

            history.append({
                "heard": text,
                "result": result
            })

        self.running = False

        return {
            "status": "jarvis_mode_finished",
            "history": history
        }

    def should_stop(self, text):
        text = text.lower()

        stop_words = [
            "parar",
            "sair",
            "desligar",
            "terminar",
            "para hermes",
            "desliga hermes",
            "sair do modo jarvis"
        ]

        return any(word in text for word in stop_words)
