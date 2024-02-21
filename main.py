import os
os.environ["SUNO_USE_SMALL_MODELS"] = "True"
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Hi, my name is Suno. And, uh — and I like pizza. [laughs] 
     Im here to help you in whatever you need
"""
audio_array = generate_audio(text_prompt,history_prompt="v2/en_speaker_9")

# save audio to disk
write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
Audio(audio_array, rate=SAMPLE_RATE)