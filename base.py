import multiprocessing
import time
import unittest

import requests
from api_server import FLASK_APP_PORT, FLASK_APP_HOST
from api_server import app as flask_app
from api_server import gen_md5, gen_random_string, get_sign


def run_flask():
    flask_app.run(FLASK_APP_HOST, FLASK_APP_PORT)


class ApiServerUnittest(unittest.TestCase):
    """ Test case class that sets up an HTTP server which can be used within the tests
    """

    def setUpClass(self):
        self.host = "http://127.0.0.1:5000"
        self.flask_process = multiprocessing.Process(
            target=run_flask
        )
        self.flask_process.start()
        time.sleep(0.1)
        self.api_client = requests.Session()

    def tearDownClass(self):
        self.flask_process.terminate()

    # def get_token(self, user_agent, device_sn, os_platform, app_version):
    #     url = "%s/api/get-token" % self.host
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'User-Agent': user_agent,
    #         'device_sn': device_sn,
    #         'os_platform': os_platform,
    #         'app_version': app_version
    #     }
    #     data = {
    #         'sign': get_sign(device_sn, os_platform, app_version)
    #     }
    #     resp = self.api_client.post(url, json=data, headers=headers)
    #     resp_json = resp.json()
    #     self.assertTrue(resp_json["success"])
    #     self.assertIn("token", resp_json)
    #     self.assertEqual(len(resp_json["token"]), 16)
    #
    #     return resp_json["token"]
    #
    # def get_authenticated_headers(self):
    #     user_agent = 'iOS/10.3'
    #     device_sn = gen_random_string(15)
    #     os_platform = 'ios'
    #     app_version = '2.8.6'
    #
    #     token = self.get_token(user_agent, device_sn, os_platform, app_version)
    #     headers = {
    #         'device_sn': device_sn,
    #         'token': token
    #     }
    #     return headers
