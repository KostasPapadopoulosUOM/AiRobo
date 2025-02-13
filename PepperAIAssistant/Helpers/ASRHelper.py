import threading


class ASRHelper:
    shouldListen = False

    def __init__(self, session, memoryHelper):
        #Initialize the ASR to recognize English
        self.timer = None
        self.asr = session.service("ALSpeechRecognition")
        if self.asr:
            self.asr.setLanguage("English")
        self.memoryHelper = memoryHelper
        self.subscriber = self.memoryHelper.memory.subscriber("WordRecognized")
        self.callback = None

    #Listen for specific words provided in the vocabulary and execute the callback when a word is recognized.
    def Listen(self, vocabulary, callback, timeout, callbackTimeout):
        if self.asr:
            print("Listening...")
            self.shouldListen = True
            self.asr.pause(True)
            self.asr.setVocabulary(vocabulary, True)
            self.asr.subscribe(self.__class__.__name__)
            self.asr.pause(False)
            self.callback = callback
            self.subscriber.signal.connect(self.onWordRecognized)
            self.timer = threading.Timer(timeout, callbackTimeout)
            self.timer.start()
    #Stop the robot from listening.
    def StopListening(self):
        if self.asr:
            if self.timer:
                self.timer.cancel()
            self.asr.pause(True)
            self.shouldListen = False

    #Internal method to the class used as a system callback to filter the words.
    def onWordRecognized(self, result):
        if self.callback and self.shouldListen:
            if self.timer:
                self.timer.cancel()
            self.callback("What is the name of the first human?", 100)
