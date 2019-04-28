import multiprocessing
import time

import requests

from api_server import app as flask_app, FLASK_APP_HOST, FLASK_APP_PORT

import pytest


def run_flask():
    flask_app.run(FLASK_APP_HOST, FLASK_APP_PORT)


@pytest.fixture
def server():
    flask_process = multiprocessing.Process(
        target=run_flask
    )
    flask_process.start()
    time.sleep(1)
    api_client = requests.Session()
    yield api_client
    flask_process.terminate()
