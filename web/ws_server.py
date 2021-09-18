#!/usr/bin/env python

import asyncio
import websockets

async def hello(websocket, path):
    while True:
        try:
            name = await websocket.recv()
        except websockets.ConnectionClosed:
            print(f"Terminated")
            break

        name = name.lower().strip()

        if name == "yes":
            reply = f"Thanks for submission! Realy apreaciated"
        elif name == "no":
            reply = f"What was it then please?"
        else:
            reply = "Sorry I don't understand"

        await websocket.send(reply)
        print(f"> {reply}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())