import requests
import base64
import unittest
from database import db 

URI = "http://localhost:3001/"

class Testing(unittest.TestCase):
    def test_get_song(self):
        """
        Test that a user can get songs from the service and listen to them.\n
        NOTE that this test only passes if the song "good 4 u" is on the database,
            you can add it by running upload_song() in add_songs.py
        """
        # Set endpoint and re
        song_name = "good 4 u"
        endpoint = URI + f"/get_song?title={song_name}"

        # Post request to user microservice
        rsp  = requests.get(endpoint)
        data = rsp.json()["data"]
        # Decode the data from base 64
        song = base64.b64decode(data)
        # Open file in write binary mode
        file = open("rsp: good 4 u.wav","wb")
        file.write(song)
        file.close()
        # Check song was successfully recieved
        self.assertEqual(rsp.status_code,200)