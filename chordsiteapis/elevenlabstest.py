from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key='sk_1dfd5509a46af95591033f4f0639adb7b5d680b60d88aff4'
)

audio = client.generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Rachel",
  model="eleven_multilingual_v2"
)
play(audio)