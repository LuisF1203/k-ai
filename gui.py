import customtkinter
import requests
import json
import os
os.environ["SUNO_USE_SMALL_MODELS"] = "True"
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
from playsound import playsound

preload_models()

url = "http://localhost:11434/api/generate"

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1080x720")

def button_function():
    print("button pressed")
    entered_text = textEntry.get()
    print(entered_text)
    questionText.configure(text="you: "+entered_text)
    data = {
    "model": "mistral",
    "prompt": entered_text
    }
    headers = {
    "Content-Type": "application/json"
    }

    responseAi(url,data,headers)
    
    questionText.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)
    responseText.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)


def responseAi(url,data,headers):
    print(data)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        # Obtener las líneas del contenido de la respuesta
        lines = response.text.strip().split('\n')

        # Convertir cada línea a un objeto JSON y almacenarlo en un array
        jsonArray = [json.loads(line) for line in lines]

        # Concatenar todas las respuestas en un solo string
        all_responses = ''.join([jsonObj.get('response', '') for jsonObj in jsonArray])

        # Imprimir el string con todas las respuestas
        print(all_responses)
        responseText.configure(text="ai: "+all_responses)
        # generate audio from text
        text_prompt = all_responses
        audio_array = generate_audio(text_prompt,history_prompt="v2/en_speaker_9")

        # save audio to disk
        write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
        
        # play text in notebook
        Audio(audio_array, rate=SAMPLE_RATE)
        playsound("bark_generation.wav")
    else:
        print(f"Error en la solicitud. Código de respuesta: {response.status_code}")




# Use CTkButton instead of tkinter Button
textEntry=customtkinter.CTkEntry(master=app,placeholder_text="Ask me anything...")
button = customtkinter.CTkButton(master=app, text="Send", command=button_function)
questionText=customtkinter.CTkLabel(master=app, text="")
responseText=customtkinter.CTkLabel(master=app, text="")

textEntry.place(relx=0.1, rely=0.5, anchor=customtkinter.CENTER)
button.place(relx=0.1, rely=0.6, anchor=customtkinter.CENTER)



app.mainloop()