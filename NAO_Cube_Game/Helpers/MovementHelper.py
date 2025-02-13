class MovementHelper:
    def __init__(self, session):
        self.LastAnimation = None
        self.movement = session.service("ALAnimationPlayer")
        self.motion = session.service("ALMotion")

    def __del__(self):
        if self.LastAnimation:
            self.LastAnimation.cancel()
            
    #Helper method to allow the robot to move.
    def Animation(self, animation):
        if self.movement:
            self.LastAnimation = self.movement.run(animation, _async=True)

    #Helper method to stop robot's movement.
    def StopAnimation(self):
        if self.LastAnimation:
            self.LastAnimation.cancel()

    def WakeUp(self):
        if not self.motion.robotIsWakeUp():
            self.motion.wakeUp()

    def Rest(self):
        if self.motion.robotIsWakeUp():
            self.motion.rest()

