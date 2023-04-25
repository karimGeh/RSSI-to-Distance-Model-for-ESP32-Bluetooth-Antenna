from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from handlers import Handlers

routesObj = dict(
    saveScan=dict(path="/save-scan", method="POST", handler=Handlers.saveScan),
    setDistance=dict(path="/set-distance", method="POST", handler=Handlers.setDistance),
    saveReadings=dict(
        path="/save-readings", method="POST", handler=Handlers.saveReadings
    ),
    startRecording=dict(
        path="/start-recording", method="POST", handler=Handlers.startRecording
    ),
    stopRecording=dict(
        path="/stop-recording", method="POST", handler=Handlers.stopRecording
    ),
    resetCounter=dict(
        path="/reset-counter", method="POST", handler=Handlers.resetCounter
    ),
)


app = FastAPI()


for key, routeObj in routesObj.items():
    route = APIRoute(
        routeObj["path"],
        routeObj["handler"],
        methods=[routeObj["method"]],
        response_model=None,
    )
    app.routes.append(route)


@app.get("/", response_class=HTMLResponse)
def index():
    return open("./client/index.html", "r").read()


# app.mount("/", StaticFiles(directory="./client"), name="client")
