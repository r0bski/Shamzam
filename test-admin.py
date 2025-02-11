import requests
import base64
import unittest
from database import db 

URI = "http://localhost:3000/"

class Testing(unittest.TestCase):
    def test_upload(self):
        """
        Test that an adimn can add songs to the database using the admin microservice.
        """
        # Set the endpoint
        endpoint = URI + "upload_wav"

        file_name = "Dont Look Back In Anger.wav"
        song_name = "Don't Look Back In Anger"

        # Open and read wav file in binary mode
        f = open(f"music/{file_name}","rb")
        wav = f.read()
        f.close()

        # Encode wav data into base64 so it can be posted in json
        music = base64.b64encode(wav).decode("ascii")
        # Define header and json content
        hdrs = {"Content-Type":"application/json"}
        js = {"title":song_name,
            "artist":"Oasis",
            "filename":file_name,
            "data":music}
        
        # Post json to microservice and store the reponce
        rsp  = requests.post(endpoint,headers=hdrs,json=js)
        # Test if song was successfully added to db
        self.assertEqual(rsp.status_code,201)

    def test_delete(self):
        """
         Test that an adimn can delete songs from the database using the admin microservice.
        """
        # Set endpoint
        endpoint = URI + "delete"
        song_name = "Don't Look Back In Anger"
        # define header and json content
        hdrs = {"Content-Type":"application/json"}
        js = {"title":song_name}
        # Post json
        rsp  = requests.post(endpoint,headers=hdrs,json=js)
        # Test that the song was successfully deleted
        self.assertEqual(rsp.status_code,200)

        
