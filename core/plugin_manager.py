import os

class PluginManager:

    def load(self):
        print("A procurar Skills...")

        path = "skills"

        for folder in os.listdir(path):
            if os.path.isdir(os.path.join(path, folder)):
                print(f"✓ {folder}")
