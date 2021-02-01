import json
import multiprocessing
import os
import time

import requests
import uvicorn

from app.api import app
from app.communication import ProcessToDaemonCommunication
from lib.settings import API_PORT

if "PRE_COMMIT" in os.environ:
    from test_libs import DOCKER_TEST_HEADERS, DOCKER_TEST_URL
else:
    from tests.test_libs import DOCKER_TEST_HEADERS, DOCKER_TEST_URL

"""
--------------------------------------------------------------------------------
"""


def _start_api(queue, return_queue):
    app.api_queue = ProcessToDaemonCommunication(queue, return_queue)
    uvicorn.run(app, host="0.0.0.0", port=API_PORT, log_level="info")


def test_ping_container():
    api_to_manager_queue = multiprocessing.Queue()
    manager_to_api_queue = multiprocessing.Queue()
    api_process = multiprocessing.Process(
        target=_start_api,
        args=(api_to_manager_queue, manager_to_api_queue),
    )
    api_process.start()
    time.sleep(0.1)

    response = requests.request(
        "GET",
        DOCKER_TEST_URL + "_ping",
        headers=DOCKER_TEST_HEADERS,
        timeout=60,
    )
    api_process.terminate()
    api_process.join()

    data = json.loads(response.text)
    is_ok = data["status"] == "ok"
    assert is_ok
