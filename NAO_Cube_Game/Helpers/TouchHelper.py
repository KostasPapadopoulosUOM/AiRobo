class TouchHelper:
    isDetecting = False

    #Initialize all the callbacks for touch sensors.
    def __init__(self, memoryHelper):
        self.LeftHandTouchedCallback = None
        self.RightHandTouchedCallback = None
        self.HeadTouchedCallback = None
        self.touch = memoryHelper.memory.subscriber("TouchChanged")
        self.id = self.touch.signal.connect(self.onTouched)
        self.isDetecting = False

    def __del__(self):
        self.StopDetecting()

    #Setup of head sensor callback.
    def HeadTouched(self, callback):
        self.HeadTouchedCallback = callback

    #Setup of left hand sensor callback.
    def LeftHandTouched(self, callback):
        self.LeftHandTouchedCallback = callback
    
    #Setup of right hand sensor callback.
    def RightHandTouched(self, callback):
        self.RightHandTouchedCallback = callback

    #Internal method to filter the sensor touched and redirect to the correct callbac.
    def onTouched(self, value):
        if self.touch and self.isDetecting and value[0][1]:
            if value[0][0] == "LArm" and self.LeftHandTouchedCallback:
                print("Touched: " + str(value[0][0]))
                self.LeftHandTouchedCallback()
            elif value[0][0] == "RArm" and self.RightHandTouchedCallback:
                print("Touched: " + str(value[0][0]))
                self.RightHandTouchedCallback()
            elif value[0][0] == "Head" and self.HeadTouchedCallback:
                print("Touched: " + str(value[0][0]))
                self.HeadTouchedCallback()

    #Start detecting touches. (Enables the filter)
    def StartDetecting(self):
        self.isDetecting = True

    #Stop detecting touches. (Disables the filter)
    def StopDetecting(self):
        self.isDetecting = False
