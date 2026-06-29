from app.core.agents.base_agent import BaseAgent


def register(brain, bus, memory):

    def on_input(data):
        print(f"[PLUGIN] received: {data}")

        if "autoagent" in data:
            agent = BaseAgent(
                "plugin_agent",
                memory,
                brain.logger,
                bus,
                brain
            )

            brain.register_agent("plugin_agent", agent)

    bus.subscribe("input.received", on_input)

    return {"name": "logger_plugin"}
