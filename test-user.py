import requests
import base64
import unittest

URI = "http://localhost:3001/"

class Testing(unittest.TestCase):
    def test_get_song(self):
        """
        Test that a user can get songs from the service and listen to them.\n
        NOTE that this test only passes if the song "good 4 u" is on the database,
            you can add it by executing: python add_songs.py
        """
        # Set endpoint and title
        song_name = "good 4 u"
        endpoint = URI + f"/get_song?title={song_name}"

        # Post request to user microservice
        rsp = requests.get(endpoint)

        # Check song was successfully recieved
        self.assertEqual(rsp.status_code,200)

        data = rsp.json()["data"]
        # Decode the data from base 64
        song = base64.b64decode(data)
        # Write song to a new file
        file = open("rsp: good 4 u.wav","wb")
        file.write(song)
        file.close()

        # Open file and check the contents are the same as the song data
        file = open("rsp: good 4 u.wav","rb")
        self.assertIsNotNone(file)
        contents = file.read()
        file.close()
        self.assertEqual(contents, song)

    
    def test_frag_recognition(self):

        endpoint = URI + "/frag_recognition"
        file = open("music/~Blinding Lights.wav", "rb")
        frag = file.read()
        file.close()
        frag_base64 = base64.b64encode(frag).decode("ascii")
        hdr = {"Content-Type":"application/json"}
        js = {"fragment": frag_base64}
        rsp = requests.post(endpoint, headers=hdr, json=js)
        self.assertEqual(rsp.status_code, 200)

