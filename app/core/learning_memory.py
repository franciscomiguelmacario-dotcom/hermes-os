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

    def get_history(self, agent):
        logs = self.memory.get("learning_log", [])
        return [l for l in logs if l["agent"] == agent]
