# Copyright 2018 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
""" Sawtooth Inbound Transaction Queue Listener
"""

from rethinkdb import r
from sawtooth_sdk.protobuf import batch_pb2

from rbac.common.logs import get_logger
from rbac.common.sawtooth import client
from rbac.common.sawtooth import batcher
from rbac.ledger_sync.database import Database

LOGGER = get_logger(__name__)


def process(rec, database):
    """ Process inbound queue records
    """
    try:
        if "batch" not in rec or not rec["batch"]:
            database.run_query(
                database.get_table("inbound_queue").get(rec["id"]).delete()
            )
            database.run_query(database.get_table("inbound_queue_errors").insert(rec))
            return

        batch = batch_pb2.Batch()
        batch.ParseFromString(rec["batch"])
        batch_list = batcher.batch_to_list(batch=batch)
        status = client.send_batches_get_status(batch_list=batch_list)
        if status[0]["status"] == "COMMITTED":
            if "metadata" in rec and rec["metadata"]:
                data = {
                    "address": rec["address"],
                    "object_type": rec["object_type"],
                    "object_id": rec["object_id"],
                    "created_at": r.now(),
                    "updated_at": r.now(),
                    **rec["metadata"],
                }
                query = (
                    database.get_table("metadata")
                    .get(rec["address"])
                    .replace(
                        lambda doc: r.branch(
                            # pylint: disable=singleton-comparison
                            (doc == None),  # noqa
                            r.expr(data),
                            doc.merge(
                                {"metadata": rec["metadata"], "updated_at": r.now()}
                            ),
                        )
                    )
                )
                result = database.run_query(query)
                if (not result["inserted"] and not result["replaced"]) or result[
                    "errors"
                ] > 0:
                    LOGGER.warning(
                        "error updating metadata record:\n%s\n%s", result, query
                    )
            database.run_query(database.get_table("inbound_queue_archive").insert(rec))
            database.run_query(
                database.get_table("inbound_queue").get(rec["id"]).delete()
            )
        else:
            rec["error"] = get_status_error(status)
            database.run_query(database.get_table("inbound_queue_errors").insert(rec))
            database.run_query(
                database.get_table("inbound_queue").get(rec["id"]).delete()
            )
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(
            "%s exception processing inbound record:\n%s", type(err).__name__, rec
        )
        LOGGER.exception(err)


def get_status_error(status):
    """ Try to get the error from a transaction status
    """
    try:
        LOGGER.warning("Error status %s", status)
        return status[0]["invalid_transactions"][0]["message"]
    except Exception:  # pylint: disable=broad-except
        return "Unhandled error {}".format(status)


def listener():
    """ Listener for Sawtooth State changes
    """
    try:
        database = Database()
        database.connect()

        LOGGER.info("Reading queued Sawtooth transactions")
        while True:
            feed = database.run_query(database.get_table("inbound_queue"))
            count = 0
            for rec in feed:
                process(rec, database)
                count = count + 1
            if count == 0:
                break
            LOGGER.info("Processed %s records in the inbound queue", count)
        LOGGER.info("Listening for incoming Sawtooth transactions")
        feed = database.run_query(database.get_table("inbound_queue").changes())
        for rec in feed:
            if rec["new_val"] and not rec["old_val"]:  # only insertions
                process(rec["new_val"], database)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception("Inbound listener %s exception", type(err).__name__)
        LOGGER.exception(err)

    finally:
        try:
            database.disconnect()
        except UnboundLocalError:
            pass
