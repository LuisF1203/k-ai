import speech_recognition as sr
import tempfile
import os
import io
from pydub import AudioSegment
import whisper
from faster_whisper import WhisperModel
import requests
import json
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio


os.environ["SUNO_USE_SMALL_MODELS"] = "True"

preload_models()

url = "http://localhost:11434/api/generate"


headers = {
    "Content-Type": "application/json"
}



model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")



temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, "temp.wav")

listener = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            print("Say something... ")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data, format="wav")
            audio_clip.export(save_path, format="wav")
    except Exception as e:
        print(e)
    return save_path


def recognize_audio(save_path):
    segments, info = model.transcribe(save_path, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    return segments

def main():
    try:
        response = recognize_audio(listen())
        for segment in response:
                print(segment.text)
                data = {
                    "model": "mistral",
                    "prompt": segment.text
                }
                response = requests.post(url, json=data, headers=headers)
                # Verificar si la solicitud fue exitosa (código de respuesta 200)
                if response.status_code == 200:
                    # Obtener las líneas del contenido de la respuesta
                    lines = response.text.strip().split('\n')

                    # Convertir cada línea a un objeto JSON y almacenarlo en un array
                    jsonArray = [json.loads(line) for line in lines]

                    # Concatenar todas las respuestas en un solo string
                    all_responses = ''.join([jsonObj.get('response', '') for jsonObj in jsonArray])

                    # Imprimir el string con todas las respuestas
                    print(all_responses)
                    # generate audio from text
                    text_prompt = all_responses
                    audio_array = generate_audio(text_prompt,history_prompt="v2/en_speaker_9")

                    # save audio to disk
                    write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
                    
                    # play text in notebook
                    Audio(audio_array, rate=SAMPLE_RATE)
                else:
                    print(f"Error en la solicitud. Código de respuesta: {response.status_code}")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()