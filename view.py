import customtkinter
import os
from scipy.io.wavfile import write as write_wav
from threading import Thread
from playsound import playsound
from queue import Queue
import requests
import json
from tkinter import *

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



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("small example app")
        self.minsize(900, 500)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        # create 2x2 grid system



        #self.textbox = customtkinter.CTkTextbox(master=self)
        #self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")
        #self.textbox2=customtkinter.CTkEntry(master=self,placeholder_text="Ask me anything...")
        #self.textbox2.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        #self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Send")
        #self.button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    def button_callback(self):
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "mistral",
            "prompt": self.textbox2.get()
        }

        headers = {
            "Content-Type": "application/json"
        }

        self.textbox.delete("0.0","end")



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
            self.textbox.insert("insert", text_prompt + "\n")

        else:
            print(f"Error en la solicitud. Código de respuesta: {response.status_code}")
        print(self.textbox2.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()