import os
from scipy.io.wavfile import write as write_wav
from threading import Thread
from playsound import playsound
from queue import Queue
import requests
import json
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from IPython.display import Audio
import nltk  # we'll use this to split into sentences
#nltk.download('punkt')

import numpy as np

from bark.generation import (
    generate_text_semantic,
    preload_models,
)
from bark.api import semantic_to_waveform
from bark import generate_audio, SAMPLE_RATE


url = "http://localhost:11434/api/generate"
data = {
    "model": "mistral",
    "prompt": "whats the capital of russia?"
}

headers = {
    "Content-Type": "application/json"
}


response = requests.post(url, json=data, headers=headers)




def genAudio(text):
    preload_models()

    current_directory = os.getcwd()
    script = f"""{text}""".replace("\n", " ").strip()

    sentences = nltk.sent_tokenize(script)

    SPEAKER = "v2/en_speaker_9"

    audio_queue = Queue()

    def play_audio_thread():
        while True:
            audio_array, file_path = audio_queue.get()
            if audio_array is None:
                break
            write_wav(file_path, SAMPLE_RATE, audio_array)
            playsound(file_path.encode('utf-8').decode('utf-8'))

    def genExpretions(sentence):
        oldText=sentence
        newText=oldText.split(" ")
        newText[0]=newText[0]+" uh — "
        for i in range(len(newText)):
            if "," in newText[i]:
                newText[i]=newText[i]+" — [giggles] "
            if "." in newText[i]:
                newText[i]=newText[i]+" —— [chuckles] "
            if "?" in newText[i]:
                newText[i]=newText[i]+" — [sniffs] — [chuckles] "
        print(" ".join(newText))
        return(" ".join(newText))


    audio_thread = Thread(target=play_audio_thread)
    audio_thread.start()

    for pi, sentence in enumerate(sentences):
        audio_array = generate_audio(genExpretions(sentence), history_prompt=SPEAKER)
        #pieces = [audio_array, silence.copy()]
        audio_queue.put((audio_array, f"{current_directory}/audio/bark/generation-{pi}.wav"))

    # Signal the end of audio generation
    audio_queue.put((None, None))

    # Continue with other tasks while audio is playing in the background
    audio_thread.join()

    print("sentences: ", len(sentences))





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
    genAudio(text_prompt)
    

else:
    print(f"Error en la solicitud. Código de respuesta: {response.status_code}")



