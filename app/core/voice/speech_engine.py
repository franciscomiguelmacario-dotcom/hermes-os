import os
import re
import shutil
import subprocess
import tempfile


class SpeechEngine:

    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger

    def default_config(self):
        return {
            "engine": "piper",
            "model": "data/voices/piper/pt_PT-tugao-medium.onnx",
            "speaker": None,
            "max_chars": "500"
        }

    def config(self):
        if not self.memory:
            return self.default_config()

        saved = self.memory.get("voice_config", {})
        config = self.default_config()
        config.update(saved)

        return config

    def set_value(self, key, value):
        if not self.memory:
            return {
                "status": "error",
                "message": "memory not available"
            }

        config = self.config()
        config[key] = str(value)
        self.memory.set("voice_config", config)

        return {
            "status": "voice_config_saved",
            "voice_config": config
        }

    def clean_text(self, text):
        if isinstance(text, dict):
            if "response" in text:
                text = text["response"]
            elif "message" in text:
                text = text["message"]
            elif "status" in text:
                text = f"Estado: {text['status']}"
            else:
                text = str(text)

        text = str(text)
        text = re.sub(r"\s+", " ", text).strip()

        max_chars = int(self.config().get("max_chars", "500"))

        if len(text) > max_chars:
            text = text[:max_chars].rsplit(" ", 1)[0] + "."

        return text

    def speak(self, text):
        text = self.clean_text(text)

        if not text:
            return {
                "status": "error",
                "message": "empty text"
            }

        config = self.config()
        engine = config.get("engine", "piper")

        if engine == "piper":
            result = self.speak_piper(text)
            if result["status"] == "speaking_done":
                return result

        return self.speak_fallback(text)

    def speak_piper(self, text):
        piper_bin = shutil.which("piper")

        if not piper_bin:
            return {
                "status": "error",
                "message": "piper not found"
            }

        model = self.config().get("model")

        if not model or not os.path.exists(model):
            return {
                "status": "error",
                "message": "piper model not found",
                "model": model
            }

        player = shutil.which("aplay") or shutil.which("paplay")

        if not player:
            return {
                "status": "error",
                "message": "audio player not found"
            }

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav_path = tmp.name

        try:
            command = [
                piper_bin,
                "--model", model,
                "--output_file", wav_path
            ]

            speaker = self.config().get("speaker")
            if speaker:
                command.extend(["--speaker", str(speaker)])

            subprocess.run(
                command,
                input=text,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                check=True
            )

            subprocess.run(
                [player, wav_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                check=False
            )

            return {
                "status": "speaking_done",
                "engine": "piper",
                "model": model,
                "text": text
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": "voice timeout"
            }

        except subprocess.CalledProcessError as error:
            return {
                "status": "error",
                "message": "piper failed",
                "detail": error.stderr
            }

        finally:
            if os.path.exists(wav_path):
                os.remove(wav_path)

    def speak_fallback(self, text):
        if shutil.which("spd-say"):
            subprocess.run(["spd-say", text], check=False)
            return {
                "status": "speaking_done",
                "engine": "spd-say",
                "text": text
            }

        if shutil.which("espeak"):
            subprocess.run(["espeak", "-v", "pt", "-s", "130", text], check=False)
            return {
                "status": "speaking_done",
                "engine": "espeak",
                "text": text
            }

        return {
            "status": "voice_engine_not_found",
            "message": "install piper-tts or espeak",
            "text": text
        }
