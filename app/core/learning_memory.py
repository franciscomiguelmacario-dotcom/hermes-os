class LearningMemory:

    def __init__(self, memory):
        self.memory = memory

    def record(self, agent, input_data, output):
        logs = self.memory.get("learning_log", [])

        logs.append({
            "agent": agent,
            "input": input_data,
            "output": output
        })

        self.memory.set("learning_log", logs)

    def all(self):
        return self.memory.get("learning_log", [])

    def history(self, agent):
        return [
            item for item in self.all()
            if item.get("agent") == agent
        ]
