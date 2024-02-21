from pydub import AudioSegment
from pydub.playback import play 

audio= AudioSegment.from_wav("audio.wav")
audio.export("audio1.mp3",format="mp3")
audio2=AudioSegment.from_mp3("audio1.mp3")

play(audio2)