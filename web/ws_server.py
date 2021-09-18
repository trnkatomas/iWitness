#!/usr/bin/env python
import argparse
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

async def main(host):
    async with websockets.serve(hello, host, 8765):
        await asyncio.Future()  # run forever


argsparser = argparse.ArgumentParser(description="Description is for suckers")
argsparser.add_argument("--host", default="localhost")
params = argsparser.parse_args()


asyncio.run(main(params.host))
