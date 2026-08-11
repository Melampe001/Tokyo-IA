# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
# -*- coding: utf-8 -*-
import speech_recognition as sr

def escuchar_y_convertir():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("--- NODO ESCUCHANDO (0x06) ---")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='es-ES')
        print(f"INPUT_RECONOCIDO: {texto}")
        return texto
    except:
        return "STATUS:0x05 | ERROR_ACUSTICO"

if __name__ == '__main__':
    escuchar_y_convertir()
