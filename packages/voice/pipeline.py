"""Voice pipeline template: STT -> redact -> router -> LLM -> TTS.
Plug faster-whisper (STT) and Piper (TTS) in production."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class VoiceConfig:
    stt: str = "faster-whisper"
    tts: str = "piper"
    sample_rate: int = 16000
    vad_threshold: float = 0.5

class VoicePipeline:
    def __init__(self, cfg, router, tts_speak=lambda t: t):
        self.cfg, self.router, self.tts = cfg, router, tts_speak

    def stt(self, audio: bytes) -> str:
        return audio.decode("utf-8", errors="ignore")  # template hook

    def handle(self, audio: bytes) -> dict:
        text = self.stt(audio)
        route = self.router.route(text, task_type="voice")
        reply = "[local-llm:" + route["provider"] + "] " + route["prompt"]
        return {"transcript": text, "route": route, "spoken": self.tts(reply)}
