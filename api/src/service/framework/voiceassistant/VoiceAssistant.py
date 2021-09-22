from python_helper import ObjectHelper, log
import os, sys, re, speech_recognition, pyttsx3

class VoiceAssistant:

    NO_CONTENT = '__NO_CONTENT__'
    API_KEY_LANGUAGE = 'api.language'

    KW_PYTTSX3_VOICE = 'voice'
    KW_PYTTSX3_VOICE_LIST = 'voices'

    EXCEPTION = 'Exception'
    SLEEP = ['stop','quit','exit','shut up','quiet','sleep','thanks']

    def handleCommandList(self,commandList):
        return self.run()

    def __init__(self, globals=None) :
        self.globals = globals
        self.language = 'EN-US' if ObjectHelper.isNone(globals) else self.globals.getApiSetting(VoiceAssistant.API_KEY_LANGUAGE)
        self.brain = speech_recognition
        self.sound = self.brain.Microphone
        self.listenner = self.brain.Recognizer()
        self.speaker = pyttsx3.init()
        speakerList = self.speaker.getProperty(VoiceAssistant.KW_PYTTSX3_VOICE_LIST)
        for speaker in speakerList:
            if self.language in speaker.id :
                log.debug(self.__init__, f'speaker = {speaker}')
                self.speaker.setProperty(VoiceAssistant.KW_PYTTSX3_VOICE,speaker.id)
        self.language
        self.running = False

    def run(self):
        self.awake = True
        while self.awake :
            content = self.listen()
            if content not in VoiceAssistant.SLEEP :
                self.speak(content)
            else :
                self.awake = False

    def listen(self):
        interpreted = False
        while not interpreted :
            audioContent = None
            with self.sound() as soundArround :
                print('Voice assistant ready')
                self.listenner.adjust_for_ambient_noise(soundArround)
                print('Voice assistant listenning')
                audioContent = self.listenner.listen(soundArround)
            content = VoiceAssistant.NO_CONTENT
            try :
                print('Voice assistant interpretting')
                content = self.listenner.recognize_google(audioContent,language=self.language)
                if not content == VoiceAssistant.NO_CONTENT:
                    interpreted = True
            except Exception as exception :
                log.debug(self.listen, f'{VoiceAssistant.EXCEPTION} {str(exception)}')
        log.debug(self.listen, f'content = {content}')
        return content

    def speak(self,content) :
        try :
            self.speaker.say(content)
            self.speaker.runAndWait()
        except Exception as exception :
            log.debug(self.speak, f'Speaker failed: {str(exception)}')
            import win32com.client as wincl
            speaker = wincl.Dispatch("SAPI.SpVoice")
            speaker = pyttsx3.init()
            speaker.Speak(content)

if __name__ == '__main__' :
    va = VoiceAssistant()
    va.run()
