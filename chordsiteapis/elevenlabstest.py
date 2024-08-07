from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="sk_76154558c8c61400891e00a771e9bc839b87f08901a93226"
)
audio = client.generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Rachel",
  model="eleven_multilingual_v2"
)
play(audio)