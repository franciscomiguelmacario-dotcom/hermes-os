class TaskQueue:

    def __init__(self, memory):
        self.memory = memory

    def add(self, title):
        tasks = self.memory.get("tasks", [])

        task = {
            "id": len(tasks) + 1,
            "title": title,
            "status": "pending",
            "result": None
        }

        tasks.append(task)
        self.memory.set("tasks", tasks)

        return task

    def all(self):
        return self.memory.get("tasks", [])

    def pending(self):
        return [t for t in self.all() if t["status"] == "pending"]

    def complete(self, task_id, result=None):
        tasks = self.all()

        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "done"
                task["result"] = result

        self.memory.set("tasks", tasks)

    def clear(self):
        self.memory.set("tasks", [])
        return {"status": "tasks_cleared"}
