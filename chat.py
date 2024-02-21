import requests
import json
import os
os.environ["SUNO_USE_SMALL_MODELS"] = "True"
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
# download and load all models
preload_models()

url = "http://localhost:11434/api/generate"
data = {
    "model": "mistral",
    "prompt": "hi, how are you?"
}

headers = {
    "Content-Type": "application/json"
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
