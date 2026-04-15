"""
Building BE API using websocket to send events to 
Mimicing events to UI - for real time NAS provisioning on Isilon 
"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

import yaml
from pathlib import Path
import asyncio

yaml_path = Path(__file__).resolve().parent / "events.yml"

with yaml_path.open("r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print(f'Loaded events from YAML: \n {data}')
print(data["events"]["jobId"])
for step in data["events"]["steps"]:
    print(step["step"], step["message"], step["status"])


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    req = await websocket.receive_text()
    print(f"Received provision request: {req}")

    await websocket.send_text("Provision request received. Starting NAS provision flow.")
    for step in data["events"]["steps"]:
        await asyncio.sleep(5)
        print(f"Sending step: {step}")
        await websocket.send_json(step)

    await websocket.send_text("Provision complete. Closing connection.")
    await websocket.close()