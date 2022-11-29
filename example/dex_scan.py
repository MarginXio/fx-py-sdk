#!/usr/bin/env python
# coding='uft8'

import sys
import os

import asyncio
from fx_py_sdk import scan
import logging

from fx_py_sdk.model.model import Sql
import time


async def main():
    """rpc and websocket should run at the same time"""
    logging.basicConfig(level=logging.INFO)

    ws_scan = scan.WebsocketScan()
    scan.RpcScan(ws_scan)

if __name__ == "__main__":
    """init database"""
    sql = Sql(database="fxdex")
    sql.drop_table()
    sql.create_table()  # creates tables if not exist

    """give some time for db to fully init"""
    time.sleep(10)

    """begin scan"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
