#!/usr/bin/python3


class DriveTrain:

    def __init__(self, outpin):
        self.outpin = outpin

    def export_dict(self):
        pass

    def printConfig(self):
        print("outpin:", self.outpin)

    def setPower(self, val):
        print("motor", self.outpin, "set to", val)
        # do the actual I/O here
        pass
