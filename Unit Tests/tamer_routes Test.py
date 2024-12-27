import json
import os
import random
import unittest
import requests

from Models.Tamer_Models import Tamer
from utils import general_utils, Logger


class MyTestCase(unittest.TestCase):


    def test_1_post_new_tamer(self):
        Logger.MyLogger().log(message={"Msg": "Starting test_1_post_new_tamer"})
        # Given
        base_url = ("http://" + os.environ.get('host', "localhost") + ":" + str(os.environ.get("port",8080)) +
                    "/api/" + os.environ.get("version", "v1"))
        endpoint = "/tamer"
        body = {"discord_id": general_utils.generate_id("TEST")}
        headers = {"Content-Type":"application/json"}
        # When
        response = requests.post(url=base_url+endpoint, headers=headers, data=json.dumps(body)).json()
        # Then
        Logger.MyLogger().log(message={"response":response})
        self.assertNotIn("error", response)
        self.assertIn("Message", response)

        Logger.MyLogger().log(message={"Msg": "Finished test_1_post_new_tamer"})

    def test_2_post_no_tamer(self):
        Logger.MyLogger().log(message={"Msg": "Starting test_2_post_no_tamer"})
        # Given
        base_url = ("http://" + os.environ.get('host', "localhost") + ":" + str(os.environ.get("port",8080)) +
                    "/api/" + os.environ.get("version", "v1"))
        endpoint = "/tamer"
        body = {}
        headers = {"Content-Type":"application/json"}
        # When
        response = requests.post(url=base_url+endpoint, headers=headers, data=json.dumps(body)).json()
        # Then
        Logger.MyLogger().log(message={"response":response})
        self.assertNotIn("Message", response)
        self.assertIn("error", response)
        self.assertEqual(400, response.get('error_code', 0))

        Logger.MyLogger().log(message={"Msg": "Finished test_2_post_no_tamer"})

    def test_3_get_all_tamers(self):
        Logger.MyLogger().log(message={"Msg": "Starting test_3_get_all_tamers"})
        # Given
        base_url = ("http://" + os.environ.get('host', "localhost") + ":" + str(os.environ.get("port",8080)) +
                    "/api/" + os.environ.get("version", "v1"))
        endpoint = "/tamer"
        body = {}
        headers = {"Content-Type":"application/json"}
        # When
        response = requests.get(url=base_url+endpoint, headers=headers).json()
        # Then
        Logger.MyLogger().log(message={"response":str(response)})
        self.assertIn("tamers", response)
        self.assertNotIn("error", response)

        Logger.MyLogger().log(message={"Msg": "Finished test_3_get_all_tamers"})

    def test_4_get_a_tamer(self):
        Logger.MyLogger().log(message={"Msg": "Starting test_4_get_a_tamer"})
        # Given
        base_url = ("http://" + os.environ.get('host', "localhost") + ":" + str(os.environ.get("port",8080)) +
                    "/api/" + os.environ.get("version", "v1"))
        endpoint = "/tamer"
        body = {}
        headers = {"Content-Type":"application/json"}
        response = requests.get(url=base_url+endpoint, headers=headers).json()
        Logger.MyLogger().log(message={"response": response})
        tamer = Tamer("")
        selected_tamer = random.choice(response.get('tamers', []))
        tamer.from_json(selected_tamer)

        # When
        response = requests.get(url=base_url + endpoint+"/"+tamer.tamer_id, headers=headers).json()
        # Then
        Logger.MyLogger().log(message={"response":str(response)})
        self.assertIn("tamer_id", response)
        self.assertNotIn("error", response)

        Logger.MyLogger().log(message={"Msg": "Finished test_4_get_a_tamer"})

    def test_0_demo(self):
        Logger.MyLogger().log(message={"Msg": "Starting test_0_demo"})
        # Given

        # When

        # Then
        self.assertEqual(True, True)

        Logger.MyLogger().log(message={"Msg": "Finished test_0_demo"})


if __name__ == '__main__':
    unittest.main()
