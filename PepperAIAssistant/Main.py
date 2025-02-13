# -*- coding: utf-8 -*-
from ChatGPT import ChatGPT
from Helpers import AutonomousLifeHelper, FreeTextASRHelper, MemoryHelper, TTSHelper, FaceDetectionHelper
from naoqi import qi
import time

class PepperAIAssistant:
    ip = "127.0.0.1"
    port = 9559
    # Setting up robot connection and all the related engines.
    def __init__(self):
        self.ttsStop = None
        self.tts = None

        connection_url = "tcp://" + self.ip + ":" + str(self.port)
        self.app = qi.Application([self.__class__.__name__, "--qi-url=" + connection_url])
        self.app.start()

        self.memoryHelper = MemoryHelper.MemoryHelper(self.app.session)
        self.autonomouslifeHelper = AutonomousLifeHelper.AutonomousLifeHelper(self.app.session)
        self.freeTextASRHelper = FreeTextASRHelper.FreeTextASRHelper(self.app.session)
        self.ttsHelper = TTSHelper.TTSHelper(self.app.session)
        self.faceDetectionHelper = FaceDetectionHelper.FaceDetectionHelper(self.app.session, self.memoryHelper)

        self.Initialize()

    def __del__(self):
        self.Reset()
    #When a person is detected, we start the main routine.
    def FaceDetected(self):
        self.faceDetectionHelper.StopDetecting()
        self.ttsHelper.Speak("Hi, I am Pepper. I'm a social bot that helps students to use artificial intelligence for whatever they need answers to. Ask me a question and I will try to assist you.")
        #We use the transcription engine to recognize free text.
        self.freeTextASRHelper.Listen(self.ASRCallback_Main, 5)
    #Transcription callback, we forward the request to ChatGPT and we read out the reply.
    def ASRCallback_Main(self, result):
        print("ASR Text: " + result)
        result = ChatGPT.Request("The question is: " + result + ". Before even answering the question, consider whether you have sufficient information to answer the question fully. You must answer using the following format: Enough Context: {Variable} | Reply:{Answer}. The word {Variable} should be replaced with 'True' if you have sufficient information, or the word 'False' if you don't. The word {Answer} should be replaced with the actual answer to the question.")
        if result[1] == "True" and result[2] > 70:
            self.ttsHelper.Speak(result[0] + ". Congratulations, your question was very accurate and contained enough context for the artificial intelligence to understand you.")
        else:
            self.ttsHelper.Speak("For Artificial Intelligence to understand you, before you ask the question, you need to provide it with rich and sufficient context on the topic you want to negotiate. Try to describe your question by adding more information about what you are looking for.")
            self.freeTextASRHelper.Listen(self.ASRCallback_Main, 5)
        self.Reset()

    def Reset(self):
        print("Resetting...")
        self.faceDetectionHelper.StopDetecting()
        time.sleep(15)
        print("Waiting for a new face.")
        self.faceDetectionHelper.DetectFace(self.FaceDetected)

    def Initialize(self):
        self.autonomouslifeHelper.EnableAutonomousLife()


main = PepperAIAssistant()
main.faceDetectionHelper.DetectFace(main.FaceDetected)
print("Started!")

while True:
    pass

