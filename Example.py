import playsound
import gtts
import os
import speech_recognition as sr
import time

def input_voise():
    voise_recogniser = sr.Recognizer()
    with sr.Microphone() as sourse:
        voise_recogniser.adjust_for_ambient_noise(sourse)
        audio = voise_recogniser.listen(sourse)
    try:
        voise_text = voise_recogniser.recognize_google(audio, language = 'ru')
        print(voise_text)
    except:
        print('Тишина')
        voise_text = 'Тишина'
    return voise_text

def output_voise(text):
    voise = gtts.gTTS(text, lang = 'ru')
    time1 = time.time()
    audio_file = 'audio'+ str(time1) +'.mp3'
    voise.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)

print(input_voise)