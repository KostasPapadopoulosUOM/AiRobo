class LEDHelper:
    def __init__(self, session):
        self.led = session.service("ALLeds")
    
    #Helper method to turn the leds on.
    def TurnOnLed(self, LED, Intensity, Duration):
        if self.led:
            fadeOp = self.led.fade(LED, Intensity / 100.,
                                   Duration, _async=True)
            fadeOp.wait()

    #Helper method to turn the leds off.
    def TurnOffLed(self, LED):
        if self.led:
            fadeOp = self.led.fade(LED, 0 / 100.,
                                   0, _async=True)
            fadeOp.wait()
