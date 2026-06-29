class GoalManager:

    def __init__(self, memory):
        self.memory = memory

    def set_goal(self, agent, goal):
        goals = self.memory.get("goals", {})
        goals[agent] = goal
        self.memory.set("goals", goals)

    def get_goal(self, agent):
        goals = self.memory.get("goals", {})
        return goals.get(agent)
