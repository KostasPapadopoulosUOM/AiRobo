# -*- coding: utf-8 -*-
from ChatGPT import ChatGPT
from Helpers import AutonomousLifeHelper, MemoryHelper, ASRHelper, TTSHelper, FaceDetectionHelper, \
    VisionRecognitionHelper, LEDHelper, MovementHelper, TouchHelper
from naoqi import qi
import time


class DiceStories:
    #Connect locally to the robot. Program is running in the robot, but can run outside the robot too!
    ip = "127.0.0.1"
    port = 9559

    def __init__(self):
        self.asr = None
        self.ttsStop = None
        self.tts = None

        connection_url = "tcp://" + self.ip + ":" + str(self.port)
        #Connect to the robot.
        self.app = qi.Application([self.__class__.__name__, "--qi-url=" + connection_url])
        self.app.start()
        
        #Initialize all the helper methods. (Read each helper for more information).
        self.autonomouslifeHelper = AutonomousLifeHelper.AutonomousLifeHelper(self.app.session)
        self.memoryHelper = MemoryHelper.MemoryHelper(self.app.session)
        self.asrHelper = ASRHelper.ASRHelper(self.app.session, self.memoryHelper)
        self.ttsHelper = TTSHelper.TTSHelper(self.app.session)
        self.ledHelper = LEDHelper.LEDHelper(self.app.session)
        self.faceDetectionHelper = FaceDetectionHelper.FaceDetectionHelper(self.app.session, self.memoryHelper)
        self.movementHelper = MovementHelper.MovementHelper(self.app.session)
        self.touchHelper = TouchHelper.TouchHelper(self.memoryHelper)
        self.touchHelper.HeadTouched(self.HeadTouched)
        self.touchHelper.StartDetecting()
        self.visionRecognitionHelper = VisionRecognitionHelper.VisionRecognitionHelper(self.app.session,
                                                                                       self.memoryHelper)
        self.Initialize()

    def __del__(self):
        self.Reset()
    #Backup touch sensors as bypass for listening (Used in noisy environments.)
    def RightHandTouched(self):
        self.ASRCallback_Main("No", 1)
    #Backup touch sensors as bypass for listening (Used in noisy environments.)
    def LeftHandTouched(self):
        self.ASRCallback_Main("Yes", 1)

    def HeadTouched(self):
        self.Reset()
    #Start the game when someone is infront of the robot.
    def FaceDetected(self):
        self.faceDetectionHelper.StopDetecting()
        self.ttsHelper.Speak("Hello! I am the sun. For years, I have been lighting up Rhodes and have witnessed many stories. Would you like to play a game about ancient Rhodes?")
        self.touchHelper.RightHandTouched(self.RightHandTouched)
        self.touchHelper.LeftHandTouched(self.LeftHandTouched)
        self.asrHelper.Listen(["yes", "no"], self.ASRCallback_Main, 30, self.Reset)
    #Listen for a response and play the game or reset for a new player.
    def ASRCallback_Main(self, result, confidence):
        if result == "ναι" and confidence > 0.5:
            self.touchHelper.RightHandTouched(None)
            self.touchHelper.LeftHandTouched(None)
            self.asrHelper.StopListening()
            self.ttsHelper.Speak("Great! Roll the dice with the heroes.")
            self.visionRecognitionHelper.DetectImage(["athena", "poseidon", "zeus"], self.ImageRecognition_1stDice, 90, self.Reset)
        elif result == "όχι" and confidence > 0.5:
            self.touchHelper.RightHandTouched(None)
            self.touchHelper.LeftHandTouched(None)
            self.asrHelper.StopListening()
            self.ttsHelper.Speak("No worries! Next time.")
            self.Reset()
    #First image detection, store it and ask for a second image.
    def ImageRecognition_1stDice(self, result):
        self.visionRecognitionHelper.StopDetecting()
        self.memoryHelper.memory.insertData("Image1", result)
        self.ttsHelper.Speak("Great! Now roll the dice with the technologies.")
        self.visionRecognitionHelper.DetectImage(["tiktok", "playstation", "smartphone"], self.ImageRecognition_2ndDice, 90, self.Reset)

    #Second image detection.
    def ImageRecognition_2ndDice(self, result):
        self.visionRecognitionHelper.StopDetecting()
        self.memoryHelper.memory.insertData("Image2", result)
        self.ttsHelper.Speak("Perfect! Give me some time to think of a story.")
        self.movementHelper.Animation("animations/Stand/BodyTalk/Thinking/ThinkingLoop_1")
        self.ledHelper.TurnOnLed("EarLeds", 100, 10)
        #Loading up chat-gpt for a response.
        content = "Tell a funny story in Greek about " + self.memoryHelper.GetMemoryEntry(
            "Image1") + ", " + self.memoryHelper.GetMemoryEntry("Image2") + " that takes place in the Greek island of Rhodes during the ancient times. Use 200 words at max."
        result = ChatGPT.Request(content)
        self.movementHelper.StopAnimation()
        self.ledHelper.TurnOffLed("EarLeds")
        if result == "":
             self.ttsHelper.Speak("Unfortunately, I couldn't come up with a story.")
        else:
             #Speak chat gpt story.
             self.ttsHelper.Speak(result)
             self.ttsHelper.Speak("That was my story. Thank you for your time!")
        self.Reset()

    #Resets the round, reinitializing anything that needs cleanup.
    def Reset(self):
        print("Resetting...")
        self.touchHelper.RightHandTouched(None)
        self.touchHelper.LeftHandTouched(None)
        self.movementHelper.StopAnimation()
        self.memoryHelper.ClearMemory()
        self.asrHelper.StopListening()
        self.faceDetectionHelper.StopDetecting()
        self.visionRecognitionHelper.StopDetecting()
        self.ledHelper.TurnOffLed("EarLeds")
        time.sleep(15)
        self.faceDetectionHelper.DetectFace(self.FaceDetected)

    #Basic initialization for startup.
    def Initialize(self):
        self.memoryHelper.ClearMemory()
        self.movementHelper.WakeUp()
        self.autonomouslifeHelper.EnableAutonomousLife()
