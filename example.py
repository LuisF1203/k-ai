from transformers import AutoProcessor, BarkModel
import scipy


expretions=["[chuckles]", "[giggles]","[laughs uncontrollably]","[sniffs]","[sighs heavily]","[whispers]","[laughs playfull]","[sings]","[raps]","[beat]","[taps boot]","[sings softly]","[sways to rhythm]","[beep]"]


def generate_audio(text,preset,output):
    processor=AutoProcessor.from_pretrained("suno/bark")
    model=BarkModel.from_pretrained("suno/bark")
    model.to("cuda")
    inputs=processor(text,voice_preset=preset)
    for k,v in inputs.items():
        inputs[k] = v.to("cuda")
    audio_array=model.generate(**inputs)
    audio_array=audio_array.cpu().numpy().squeeze()
    sample_rate=model.generation_config.sample_rate
    scipy.io.wavfile.write(output,rate=sample_rate,data=audio_array)







    

def genExpretions():
    expretions="[chuckles] [giggles] [laughs uncontrollably] [sniffs] [sighs heavily] [whispers] [laughs playfull] [sings] [raps] [beat] [taps boot] [sings softly] [sways to rhythm] [beep]"
    oldText="Hello! I'm just a computer program, so I don't have the ability to feel emotions or have a physical state. But I'm here and ready to help answer any questions you might have. Let me know if there's something specific you'd like to know about!"
    newText=oldText.split(" ")
    newText[0]=newText[0]+" uh — "
    for i in range(len(newText)):
        if "." in newText[i]:
            newText[i]=newText[i]+" [chuckles] "
    return(" ".join(newText))

if __name__ == "__main__":
    print(genExpretions())
    generate_audio(
        text=genExpretions(),
        preset="v2/en_speaker_9",
        output="output.wav"
    )