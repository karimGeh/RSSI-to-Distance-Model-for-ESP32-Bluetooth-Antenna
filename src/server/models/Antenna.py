from pydantic import BaseModel
import os


class Antenna(BaseModel):
    antennaId: str
    readings: list = []

    def addScan(self, scan):
        self.readings += [scan]

    def saveReadingsToCSVFile(self, directory: str):
        if len(self.readings) == 0:
            return
        filePath = f"{directory}/{self.antennaId}.csv".replace(":", "-")
        # create if not exist directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filePath, "a") as f:
            for scan in self.readings:
                distance = scan["distance"]
                rssi = scan["rssi"]
                reading = f"{distance},{rssi}\n"
                f.write(reading)
