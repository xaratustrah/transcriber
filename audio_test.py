#!/usr/bin/env python
"""


Xaratustrah 2016

"""

import speech_recognition as sr


def rec(a, b):
    print(a, b)


def recognize(recognizer_instance, audio_data):
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = str(recognizer_instance.recognize_google(audio_data))
        print(text)
        if 'on' in text.lower():
            print('Turning on!')
        if 'off' in text.lower():
            print('Turning off!')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def main():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.listen_in_background(source, recognize)


# ----------------------------

if __name__ == '__main__':
    main()
