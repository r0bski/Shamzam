from flask import Flask, request, jsonify
from database import db
import base64
import os
import requests

KEY = os.environ["AUDD_KEY"]
AUDD_API = "https://api.audd.io/"

app = Flask(__name__)

@app.route('/get_song', methods=['GET'])
def get_song():
    title = request.args.get("title")
    if title is None:
        return jsonify({"error": "No 'title' found in the request"}), 400
    id = db.get_id(title)
    row = db.lookup(id)
    if row is None or id is None:
        return jsonify({"error": "Song not found in database"}), 404
    data = row["data"]
    return jsonify({"message":"Successfully retreved song", "data":data}), 200

@app.route('/frag_recognition', methods=['POST'])
def frag_recognition():
    """_summary_

    Expects:
    {
    fragment:<base 64 song data>
    }
    """
    js = request.get_json()
    if js is None:
        return jsonify({"error": "No JSON payload"}), 400
    # Get base 64 encoded song fragment
    frag = js.get("fragment")
    if frag is None:
        return jsonify({"error": "Song fragment data not in JSON payload"}), 400
    result = audd_recognition(frag)
    if result is None:
        return jsonify({"error": "Frailed to recognise song"}), 500
    title = result["result"]["title"]
    id = db.get_id(title)
    if id is None:
        return jsonify({"error": f"Song '{title}' not found in database"}), 404
    song_dict = db.lookup(id)
    artist = song_dict["artist"]
    data = song_dict["data"]
    return jsonify({"message":f"Successfully retreved '{title}' by {artist}", "data":data})



def audd_recognition(frag:base64):
    hdr = {"Content-Type":"multipart/form-data"}
    data = {
        'api_token': KEY,
        'return': 'apple_music,spotify',
    }
    frag_wav = base64.b64decode(frag)
    result = requests.post(AUDD_API , headers=hdr, data=data, files=frag_wav)
    print(result)
    if result.status_code == 200:
        return result.content
    else:
        return None




if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)