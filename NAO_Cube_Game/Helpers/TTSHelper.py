class TTSHelper:
    def __init__(self, session):
        self.tts = session.service("ALAnimatedSpeech")
    
    #Allow the robot to use the text to speech functionality and speak a sentence provided in text.
    def Speak(self, text):
        if self.tts:
            print("Speak: " + text)
            self.tts.say(text)
