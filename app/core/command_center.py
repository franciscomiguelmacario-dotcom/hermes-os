class CommandCenter:

    def __init__(self, brain, logger, memory, bus):
        self.brain = brain
        self.logger = logger
        self.memory = memory
        self.bus = bus

    def execute(self, cmd):

        cmd = cmd.strip()

        if cmd == "status":
            return {
                "system": self.memory.get("system_status"),
                "goals": self.memory.get("goals")
            }

        if cmd == "memory":
            return self.memory.dump()

        if cmd == "agents":
            return list(self.brain.agents.keys())

        if cmd.startswith("set "):
            _, k, v = cmd.split(" ", 2)
            self.memory.set(k, v)
            return f"{k}={v}"

        if cmd.startswith("goal "):
            _, agent, goal = cmd.split(" ", 2)
            self.brain.goals.set_goal(agent, goal)
            return f"{agent} -> {goal}"

        if cmd.startswith("event "):
            _, e = cmd.split(" ", 1)
            self.bus.publish("cli.event", {"event": e})
            return f"event: {e}"

        if cmd == "learn":
            return self.brain.learner.memory.get("learning_log", [])

        if cmd.startswith("history "):
            _, agent = cmd.split(" ", 1)
            return self.brain.learner.get_history(agent)

        if cmd.startswith("spawn "):
            _, name = cmd.split(" ", 1)

            agent = self.brain.factory.create(
                name,
                self.memory,
                self.bus,
                self.brain.goals,
                self.brain.learner
            )

            self.brain.agents[name] = agent
            return f"spawned {name}"

        if cmd == "help":
            return ["status", "memory", "agents", "set", "goal", "event", "learn", "history", "spawn", "exit"]

        return self.brain.process(cmd)
