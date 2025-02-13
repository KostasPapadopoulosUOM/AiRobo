class AutonomousLifeHelper:
    def __init__(self, session):
        self.autonomouslife = session.service("ALAutonomousLife")
        self.basicawareness = session.service("ALBasicAwareness")

    #Helper method to setup the robots autonomous life subsystem.
    def EnableAutonomousLife(self):
        if self.autonomouslife:
            self.autonomouslife.setAutonomousAbilityEnabled("AutonomousBlinking", True)
            self.autonomouslife.setAutonomousAbilityEnabled("BackgroundMovement", True)
            self.autonomouslife.setAutonomousAbilityEnabled("BasicAwareness", True)
            self.basicawareness.setEngagementMode("SemiEngaged")
            self.autonomouslife.setAutonomousAbilityEnabled("ListeningMovement", True)
            self.autonomouslife.setAutonomousAbilityEnabled("SpeakingMovement", True)
