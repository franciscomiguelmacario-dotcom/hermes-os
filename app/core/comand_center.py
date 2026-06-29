class CommandCenter:

    def __init__(self, brain, logger, shared_memory, bus):
        self.brain = brain
        self.logger = logger
        self.memory = shared_memory
        self.bus = bus

    def execute(self, cmd):

        if cmd == "status":
            return self.memory.dump()

        if cmd == "memory":
            return self.memory.dump()

        if cmd == "agents":
            return list(self.brain.agents.keys())

        if cmd.startswith("set "):
            parts = cmd.split(" ", 2)
            if len(parts) == 3:
                _, key, value = parts
                self.memory.set(key, value)
                return f"{key} set to {value}"

        if cmd == "help":
            return "status | memory | agents | set key value | exit"

        return self.brain.process(cmd)
