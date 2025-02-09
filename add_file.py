import requests
import base64

from database import db 

upload = "http://localhost:3000/upload_wav"

def test_upload():
    db.clear()
    file_name="Dont_Look_Back_In_Anger.wav"

    f = open(f"music/{file_name}","rb")
    wav = f.read()
    f.close()

    music = base64.b64encode(wav).decode("ascii")

    hdrs = {"Content-Type":"application/json"}
    js = {"title":"Don't Look Back In Anger",
        "artist":"Oasis",
        "filename":file_name,
        "data":music}
    
    rsp  = requests.post(upload,headers=hdrs,json=js)
    print(rsp.content)
    print(db.lookup(1))

if __name__ == "__main__":
    #test_upload()
    print(db.lookup(2))
