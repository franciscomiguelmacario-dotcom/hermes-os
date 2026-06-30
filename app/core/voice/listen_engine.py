import json
import os
import queue
import time


class ListenEngine:

    def __init__(self, memory=None, logger=None):
        self.memory = memory
        self.logger = logger

    def default_config(self):
        return {
            "model": "data/models/vosk/vosk-model-small-pt-0.3",
            "samplerate": "16000",
            "seconds": "5"
        }

    def config(self):
        config = self.default_config()

        if self.memory:
            saved = self.memory.get("listen_config", {})
            config.update(saved)

        return config

    def set_value(self, key, value):
        config = self.config()
        config[key] = str(value)

        if self.memory:
            self.memory.set("listen_config", config)

        return {
            "status": "listen_config_saved",
            "listen_config": config
        }

    def listen_once(self, seconds=None):
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
        except Exception as error:
            return {
                "status": "error",
                "message": "missing voice input dependencies",
                "detail": str(error)
            }

        config = self.config()
        model_path = config.get("model")
        samplerate = int(config.get("samplerate", "16000"))
        seconds = int(seconds or config.get("seconds", "5"))

        if not os.path.exists(model_path):
            return {
                "status": "error",
                "message": "vosk model not found",
                "model": model_path
            }

        audio_queue = queue.Queue()
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, samplerate)

        def callback(indata, frames, time_info, status):
            audio_queue.put(bytes(indata))

        text_parts = []
        end_time = time.time() + seconds

        try:
            with sd.RawInputStream(
                samplerate=samplerate,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=callback
            ):
                while time.time() < end_time:
                    data = audio_queue.get()

                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()

                        if text:
                            text_parts.append(text)

                final = json.loads(recognizer.FinalResult())
                final_text = final.get("text", "").strip()

                if final_text:
                    text_parts.append(final_text)

        except Exception as error:
            return {
                "status": "error",
                "message": "microphone listen failed",
                "detail": str(error)
            }

        text = " ".join(text_parts).strip()

        return {
            "status": "ok" if text else "no_speech_detected",
            "seconds": seconds,
            "text": text
        }
