class TaskQueue:

    def __init__(self, memory):
        self.memory = memory

    def add(self, title):
        tasks = self.memory.get("tasks", [])

        task = {
            "id": len(tasks) + 1,
            "title": title,
            "status": "pending"
        }

        tasks.append(task)
        self.memory.set("tasks", tasks)

        return task

    def all(self):
        return self.memory.get("tasks", [])

    def pending(self):
        return [t for t in self.all() if t["status"] == "pending"]

    def complete(self, task_id):
        tasks = self.all()

        for task in tasks:
            if task["id"] == task_id:
                task["status"] = "done"

        self.memory.set("tasks", tasks)
