class AutopilotEngine:

    def __init__(self, decisions, tasks, workflows, logger):
        self.decisions = decisions
        self.tasks = tasks
        self.workflows = workflows
        self.logger = logger

    def run_once(self):
        decision = self.decisions.next_action()
        action = decision.get("action", "")

        if action.startswith("set-business "):
            return {
                "status": "needs_user_input",
                "decision": decision
            }

        if action == "tasks":
            return {
                "status": "waiting_pending_tasks",
                "decision": decision,
                "pending_tasks": self.tasks.pending()
            }

        if action.startswith("task "):
            title = action.replace("task ", "", 1)
            task = self.tasks.add(title)

            return {
                "status": "task_created",
                "decision": decision,
                "task": task
            }

        if action.startswith("workflow "):
            name = action.replace("workflow ", "", 1)
            result = self.workflows.run(name)

            return {
                "status": "workflow_started",
                "decision": decision,
                "result": result
            }

        return {
            "status": "unknown_action",
            "decision": decision
        }
