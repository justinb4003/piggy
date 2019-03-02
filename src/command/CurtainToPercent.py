from .BaseCommand import BaseCommand


class CurtainToPercent(BaseCommand):

    def set_curtain(self, curtain):
        self.curtain = curtain

    def set_target(self, target):
        self.target_pct = target

    def execute(self):
        # There should probably be some ramping here but that'll
        # depend entirely on the controller.`
        if (self.curtain.get_percent() < self.target_pct):
            self.curtain.set_open()
        else:
            self.curtain.set_close()

    def is_finished(self):
        if (abs(self.curtain.get_percent() - self.target_pct) < 0.10):
            return True
        return False

    def end(self):
        self.curtain.stop()
