class FaceDetectionHelper:
    shouldDetectFace = False

    #Initialize face detection.
    def __init__(self, session, memoryHelper):
        self.faceDetection = session.service("ALFaceDetection")
        self.memoryHelper = memoryHelper
        self.subscriber = self.memoryHelper.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.onFaceRecognized)
        self.callback = None

    def __del__(self):
        self.StopDetecting()

    #Start face detection.
    def DetectFace(self, callback):
        if self.faceDetection:
            self.callback = callback
            self.faceDetection.subscribe(self.__class__.__name__, 1000, 0)
            self.faceDetection.setTrackingEnabled(True)
            self.faceDetection.setRecognitionEnabled(False)
            self.shouldDetectFace = True

    #Stop face detection.
    def StopDetecting(self):
        if self.faceDetection:
            self.shouldDetectFace = False
            self.faceDetection.setTrackingEnabled(False)
            self.faceDetection.setRecognitionEnabled(False)

    #Internal method to filter face detection.
    def onFaceRecognized(self, result):
        if self.callback and self.shouldDetectFace:
            print("Face Detected!")
            self.callback()
