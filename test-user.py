import requests
import base64
import unittest
from database import db 

URI = "http://localhost:3001/"

class Testing(unittest.TestCase):
    def test_get_song(self):
        endpoint = URI + "/get_song"

        song_name = "good 4 u"
        hdrs = {"Content-Type":"application/json"}
        js = {"title":song_name}
        rsp  = requests.post(endpoint,headers=hdrs,json=js)
        data = rsp.json()["data"]
        song = base64.b64decode(data)
        file = open("rsp: good 4 u.wav","wb")
        file.write(song)
        file.close()
        self.assertEqual(rsp.status_code,200)