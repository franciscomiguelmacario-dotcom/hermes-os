class EventBus:

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event, callback):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(callback)

    def emit(self, event, data=None):
        if event in self.subscribers:
            for cb in self.subscribers[event]:
                cb(data)
