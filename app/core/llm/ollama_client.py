import json
import urllib.request
import urllib.error


class OllamaClient:

    def __init__(self, model="llama3.1:8b", host="http://localhost:11434"):
        self.model = model
        self.host = host

    def generate(self, prompt):
        url = f"{self.host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                return {
                    "status": "ok",
                    "model": self.model,
                    "response": result.get("response", "").strip()
                }

        except urllib.error.URLError as error:
            return {
                "status": "error",
                "message": "Ollama not available",
                "detail": str(error)
            }

        except Exception as error:
            return {
                "status": "error",
                "message": "Ollama request failed",
                "detail": str(error)
            }
