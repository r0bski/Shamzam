import requests
import base64
from database import db 

URI = "http://localhost:3000/"

def upload_song1():
    upload = URI + "upload_wav"

    file_name = "good 4 u.wav"
    song_name = "good 4 u"
    artist = "Olivia Rodrigo"

    f = open(f"music/{file_name}","rb")
    wav = f.read()
    f.close()

    music = base64.b64encode(wav).decode("ascii")

    hdrs = {"Content-Type":"application/json"}
    js = {"title":song_name,
        "artist":artist,
        "filename":file_name,
        "data":music}
        
    rsp  = requests.post(upload,headers=hdrs,json=js)

def upload_song2():
    upload = URI + "upload_wav"

    file_name = "Blinding Lights.wav"
    song_name = "Blinding Lights"
    artist = "The Weeknd"

    f = open(f"music/{file_name}","rb")
    wav = f.read()
    f.close()

    music = base64.b64encode(wav).decode("ascii")

    hdrs = {"Content-Type":"application/json"}
    js = {"title":song_name,
        "artist":artist,
        "filename":file_name,
        "data":music}
            
    rsp  = requests.post(upload,headers=hdrs,json=js)

if __name__ == "__main__":
    db.clear()
    upload_song1()
    upload_song2()