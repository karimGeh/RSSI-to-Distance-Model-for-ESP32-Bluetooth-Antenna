from models.Antenna import Antenna
from datetime import datetime


class State:
    def __init__(self):
        self.counter = 0
        self.maxReadings = 50
        self.isRecordingEnabled = False
        self.currentDistance = 0
        self.antennas = {
            1: Antenna(antennaId=1),
            # "ff:ff:30:02:3e:5c": Antenna(macAddress="ff:ff:30:02:3e:5c"),
            # "ff:ff:30:02:7c:e7": Antenna(macAddress="ff:ff:30:02:7c:e7"),
            # "ff:21:10:25:35:0c": Antenna(macAddress="ff:21:10:25:35:0c"),
        }

        self.startTime = None
        self.endTime = None

    def saveScan(self, scanData):
        if not self.isRecordingEnabled or self.counter >= self.maxReadings:
            return

        if self.counter == 0:
            self.startTime = datetime.now()
        if self.counter == self.maxReadings - 1:
            self.endTime = datetime.now()
            timeTaken = self.endTime - self.startTime
            timeTaken = timeTaken.total_seconds()
            print(f"Time taken: {timeTaken} seconds")

        scan = {
            "macAddress": scanData["macAddress"],
            "rssi": scanData["rssi"],
            "distance": self.currentDistance,
            "counter": self.counter,
        }
        self.antennas[scanData["antennaId"]].addScan(scan)
        self.counter += 1
        print(scan)

    def startRecording(self):
        self.isRecordingEnabled = True

    def stopRecording(self):
        self.isRecordingEnabled = False

    def setCounter(self, value):
        self.counter = value

    def setDistance(self, distance):
        self.currentDistance = distance


mainState = State()
