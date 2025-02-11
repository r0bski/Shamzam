import requests
import base64
from database import db 

URI = "http://localhost:3000/"

def upload_song():
    upload = URI + "upload_wav"

    file_name = "good 4 u.wav"
    song_name = "good 4 u"

    f = open(f"music/{file_name}","rb")
    wav = f.read()
    f.close()

    music = base64.b64encode(wav).decode("ascii")

    hdrs = {"Content-Type":"application/json"}
    js = {"title":song_name,
        "artist":"Olivia Rodrigo",
        "filename":file_name,
        "data":music}
        
    rsp  = requests.post(upload,headers=hdrs,json=js)

if __name__ == "__main__":
    upload_song()