import requests
import base64
import unittest
from database import db 

URI = "http://localhost:3000/"

class Testing(unittest.TestCase):
    def test_upload(self):
        upload = URI + "upload_wav"
        db.clear()
        file_name = "Dont_Look_Back_In_Anger.wav"
        song_name = "Don't Look Back In Anger"

        f = open(f"music/{file_name}","rb")
        wav = f.read()
        f.close()

        music = base64.b64encode(wav).decode("ascii")

        hdrs = {"Content-Type":"application/json"}
        js = {"title":song_name,
            "artist":"Oasis",
            "filename":file_name,
            "data":music}
        
        rsp  = requests.post(upload,headers=hdrs,json=js)
        self.assertEqual(rsp.status_code,201)

    def test_delete(self):
        remove = URI + "delete"
        hdrs = {"Content-Type":"application/json"}
        song_name = "Don't Look Back In Anger"
        js = {"title":song_name}
        rsp  = requests.post(remove,headers=hdrs,json=js)
        self.assertEqual(rsp.status_code,200)

        
