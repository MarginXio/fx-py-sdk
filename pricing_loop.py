#!/usr/bin/env python
# coding='uft8'
from fx_py_sdk import scan
import os
import logging
import time

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    base_url = os.environ.get("BASE_URL")

    time.sleep(10)
    pricing_scan = scan.PricingScan(base_url)
    pricing_scan.update_pricings_looped()
