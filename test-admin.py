import requests
import base64
import unittest 

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
        file = open(f"music/{file_name}","rb")
        wav = file.read()
        file.close()

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
        rsp  = requests.delete(endpoint,headers=hdrs,json=js)
        # Test that the song was successfully deleted
        self.assertEqual(rsp.status_code,200)

    def test_get_titles(self):
        """ Test that an admin can get the titles of tracks in the db
        """
        # Set endpoint
        endpoint = URI + "get_titles"
        # Send get request
        rsp = requests.get(endpoint)
        # Test that it was successful
        self.assertEqual(rsp.status_code, 200)
        data = rsp.json()
        print("Titles:", data.get("titles"))


        