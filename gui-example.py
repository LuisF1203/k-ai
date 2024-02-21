import tkinter
import tkinter.messagebox
import customtkinter
from scipy.io.wavfile import write as write_wav
from tkVideoPlayer import TkinterVideo
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
from PIL import Image
from bark import SAMPLE_RATE, generate_audio, preload_models
import requests
import json
import nltk  # we'll use this to split into sentences
from queue import Queue
from playsound import playsound
from threading import Thread

import os


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








class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=20)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="K-ai", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #self.textbox = customtkinter.CTkTextbox(self.sidebar_frame, width=300,height=300)
        #self.textbox.grid(row=1, column=0, padx=20, pady=(20, 20))



        #image_path=os.path.join(os.path.dirname(__file__),'images/ana.gif')
        #self.img=customtkinter.CTkImage(light_image=Image.open(image_path),size=(150,150))
        #self.image_label=customtkinter.CTkLabel(self,image=self.img,text="",anchor="w")
        #self.image_label.grid(row=1, column=0, padx=20, pady=(20, 100))


        self.vid_player = TkinterVideo(master=self.sidebar_frame, scaled=True, keep_aspect=True, consistant_frame_rate=True, bg="black")
        self.vid_player.set_size([120,120])
        self.vid_player.set_resampling_method(0.5)
        self.vid_player.load("ana.mp4")


        self.vid_player.grid(row=1, column=0, padx=20, pady=(50, 200))





        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))





        self.textbox3 = customtkinter.CTkTextbox(self, width=600,height=500)
        self.textbox3.grid(row=0, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")


        

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Ask me anything...")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),text="Send",command=self.send_prompt)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    
    





    
    








    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


    


















    def send_prompt(self):
        self.textbox3.delete("0.0","end")
        prompt=self.entry.get()
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "mistral",
            "prompt": prompt
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        print(prompt)
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
            print(text_prompt)
            genAudio(text_prompt)
            self.textbox3.insert("insert", text_prompt + "\n")
            self.vid_player.play()
            #genAudio(text_prompt)
            
            #audio_array = generate_audio(text_prompt,history_prompt="v2/en_speaker_9")
            # save audio to disk
            #write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
            
            # play text in notebook
            #Audio(audio_array, rate=SAMPLE_RATE)
        else:
            print(f"Error en la solicitud. Código de respuesta: {response.status_code}")



if __name__ == "__main__":
    app = App()
    app.mainloop()