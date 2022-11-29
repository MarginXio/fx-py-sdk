#!/usr/bin/env python
# coding='uft8'

import sys
import os

import asyncio
import json
from fx_py_sdk.fx_rpc.ws import FxWebsocket


async def main():
    ws_url = "ws://127.0.0.1:26657/"
    # data = {
    #     "jsonrpc": "2.0",
    #     "method": "subscribe",
    #     "params": ["tm.event='NewBlock'"],
    #     "id": 1
    # }

    data = {
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": ["tm.event='Tx'"],
        "id": 1
    }

    event = json.dumps(data).encode()
    wss = FxWebsocket(ws_url, event)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
