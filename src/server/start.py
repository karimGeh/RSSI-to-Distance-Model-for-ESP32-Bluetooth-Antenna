# with reload on save


import uvicorn

# from main import app

uvicorn.run("main:app", host="192.168.2.101", port=8000, reload=True)
