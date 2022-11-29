#!/usr/bin/env python
# coding='uft8'

"""
File periodically polls for data integrity.
If the block height increment or number of incomplete blocks exceeds a threshold, sends a warning e-mail.
"""

from datetime import datetime
import logging
import time
import pandas as pd
from fx_py_sdk.model.crud import Crud
import os

from fx_py_sdk.notify_service import send_mail


BLOCK_TIME = 3
REFRESH_INTERVAL = int(os.environ.get("INTEGRITY_REFRESH_INTERVAL", "300"))
INCOMPLETE_THRESHOLD = int(os.environ.get("INCOMPLETE_THRESHOLD", "100"))
# BLOCK_HEIGHT_DIFF_THRESOLD = REFRESH_INTERVAL // (BLOCK_TIME + 3)
BLOCK_HEIGHT_DIFF_THRESOLD = int(os.environ.get("BLOCK_HEIGHT_DIFF_THRESHOLD", "50"))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Started integrity checking loop...")
    time.sleep(10)

    crud = Crud()
    engine = crud.session.get_bind()

    df_incomplete = None
    df_max_height = None

    while True:
        logging.info("Running integrity check")

        try:
            last_check_time = time.time()
            error_messages = []

            # Compare differences in # incomplete blocks per pair
            query = """
            SELECT pair_id, COUNT(*) AS num_incomplete_blocks
            FROM block
            WHERE tx_events_processed=FALSE or block_processed=FALSE
            GROUP BY 1
            """

            df_incomplete_new = pd.read_sql(query, con=engine, index_col="pair_id")
            if df_incomplete is not None:
                df = df_incomplete_new.merge(
                    df_incomplete,
                    left_index=True, right_index=True, how="left",
                    suffixes=("", "_old"),
                )
                incomplete_diff = df["num_incomplete_blocks"] - df["num_incomplete_blocks_old"]
                incomplete_diff = incomplete_diff[incomplete_diff > INCOMPLETE_THRESHOLD]
                if not incomplete_diff.empty:
                    error_messages.append("** Number of ambiguous blocks exceeded threshold for following pairs **")
                    error_messages.append(incomplete_diff.to_string())

            df_incomplete = df_incomplete_new


            # Compare differences in maximum block height
            query = """
            SELECT pair_id, MAX(height) AS max_block_height
            FROM block
            GROUP BY 1
            """

            df_max_height_new = pd.read_sql(query, con=engine, index_col="pair_id")
            if df_max_height is not None:
                df = df_max_height_new.merge(
                    df_max_height,
                    left_index=True, right_index=True, how="left",
                    suffixes=("", "_old"),
                )
                height_diff = df["max_block_height"] - df["max_block_height_old"]
                height_diff = height_diff[height_diff < BLOCK_HEIGHT_DIFF_THRESOLD]
                if not height_diff.empty:
                    error_messages.append("** Number of blocks synced below threshold for following pairs **")
                    error_messages.append(height_diff.to_string())

            df_max_height = df_max_height_new


            # Send an email if any messages
            if error_messages:
                timestamp = datetime.now().strftime("%d%m%Y %H%M%S")
                send_mail(
                    subject=f"FX Dex DB Integrity Warning {timestamp}",
                    recipients=os.environ["GMAIL_APP_EMAIL"],
                    text="\n\n".join(error_messages)
                )
            else:
                logging.info("Integrity checks successful. No major errors detected.")

        except Exception as ex:
            logging.error(f"Exception occurred: {ex}")

        finally:
            # Sleep until next comparison
            time.sleep(REFRESH_INTERVAL)

