import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('город', 'кеша', 'инокентий', 'иннокентий', 'кишун', 'киш', 'иношопотянин'),
    "tbr": ('вода', 'водичка', 'электричество'),
    "cmds": {
        "pokazania": ('туалет', 'в туалете', 'в санузле', 'на кухне', 'в кухне', 'санузел',
                      'кухня', 'ванная'),
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def listen(audio):
    with m as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        query = r.recognize_google(audio, language='ru-RU')
        print(query)


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == "tbr" + "pokazania" or "tbr":
        speak('сколько, скажите цифру или число')
        listen()



r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    speak_engine = pyttsx3.init()

speak("Ну чё пацаны")
speak("Погнали блинб")
speak("Рассказывайте...")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop