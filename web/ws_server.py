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

        print(f"< {name}")
        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f"> {greeting}")

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())