import threading
class VisionRecognitionHelper:
    shouldDetectImage = False
    
    #Initialize the Vision Recognition to allow the cubes to be detected.
    def __init__(self, session, memoryHelper):
        self.timer = None
        self.imageDetection = session.service("ALVisionRecognition")
        self.memoryHelper = memoryHelper
        self.subscriber = self.memoryHelper.memory.subscriber("PictureDetected")
        self.callback = None

    def __del__(self):
        self.StopDetecting()

    #Start the image detection, wait for X amount of time and return the Tag provided if it matches an image.
    def DetectImage(self, tags, callback, timeout, callbackTimeout):
        if self.imageDetection:
            self.tags = tags
            self.shouldDetectImage = True
            self.signalid = self.subscriber.signal.connect(self.onImageDetected)
            self.callback = callback
            self.imageDetection.subscribe(self.__class__.__name__, 1000, 0)
            self.timer = threading.Timer(timeout, callbackTimeout)
            self.timer.start()

    #Stop image detection and close all relevant pipes.
    def StopDetecting(self):
        self.shouldDetectImage = False
        if self.imageDetection:
            try:
                if self.timer:
                    self.timer.cancel()
                self.imageDetection.disconnect()
                if self.signalid:
                    self.subscriber.signal.disconnect()
            except:
                pass

    #Internal callback used to filter the tags of the images.
    def onImageDetected(self, result):
        if len(result) > 0 and self.shouldDetectImage:
            label = str(result[1][0][0][0]).strip()
            print("Image Detected, Label: " + label)
            if label in self.tags:
                self.shouldDetectImage = False
                if self.timer:
                    self.timer.cancel()
                print("Filtered Image Detected, Label: " + label)
                if self.callback:
                    self.callback(str(result[1][0][0][0]))
