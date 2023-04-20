from fastapi import Request
from State import mainState
import json


async def _saveScan(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))
    mainState.saveScan(data)
    return {"data": data}


async def _startRecording(request: Request):
    mainState.startRecording()
    return {"success": True}


async def _stopRecording(request: Request):
    mainState.stopRecording()
    return {"success": True}


async def _resetCounter(request: Request):
    mainState.setCounter(0)
    return {"success": True}


async def _setDistance(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))
    mainState.setCounter(0)
    mainState.setDistance(data["distance"])
    return {"success": True}


async def _saveReadings(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))
    for macAddress in mainState.antennas:
        mainState.antennas[macAddress].saveReadingsToCSVFile("../data")
    return {"success": True}


class Handlers:
    saveScan = _saveScan
    startRecording = _startRecording
    stopRecording = _stopRecording
    resetCounter = _resetCounter
    setDistance = _setDistance
    saveReadings = _saveReadings
