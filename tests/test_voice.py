from packages.voice.pipeline import VoicePipeline, VoiceConfig
from packages.core.router import Router

def test_voice_roundtrip():
    vp = VoicePipeline(VoiceConfig(), Router())
    out = vp.handle(b"transfer 100 dollars")
    assert "route" in out and "spoken" in out
    assert out["route"]["provider"] == "local"
