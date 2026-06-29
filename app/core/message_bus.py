class MessageBus:

    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, callback):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    def publish(self, topic, data=None):
        for cb in self.subscribers.get(topic, []):
            cb(data)
