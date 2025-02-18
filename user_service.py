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
    """Gets a song from the database
    
    Expects:
        .../get_song?title="<some song title>"


    Returns:
        base64-encoded WAV data: Encoded song data
    """
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
    """
    Expects:
    {
      "fragment": "<base64-encoded WAV data>"
    }

    1) Decodes the base64 string and sends to Audd.io for recognition.
    2) If recognized, we get the song title from Audd.io's response.
    3) Looks up that title in the local database.
    4) If found, returns the stored data for that track.
    """
    js = request.get_json()
    if js is None:
        return jsonify({"error": "No JSON payload"}), 400

    # Get base64-encoded song fragment
    frag_base64 = js.get("fragment")
    if not frag_base64:
        return jsonify({"error": "Song fragment data not in JSON payload"}), 400

    # Recognize via Audd.io
    result = audd_recognition(frag_base64)
    if not result or 'result' not in result or not result['result']:
        return jsonify({"error": "Failed to recognize song"}), 500

    # Extract recognized song info from Audd.io response
    title = result["result"].get("title")
    if not title:
        return jsonify({"error": "Failed to parse title from Audd.io response"}), 500

    # Look up the recognized title in the local database
    track_id = db.get_id(title)
    if track_id is None:
        return jsonify({"error": f"Song '{title}' not found in database"}), 404

    song_dict = db.lookup(track_id)
    if not song_dict:
        return jsonify({"error": "Song not found in database"}), 404

    artist = song_dict.get("artist", "Unknown Artist")
    data = song_dict.get("data", "")

    return jsonify({
        "message": f"Successfully retrieved '{title}' by {artist}",
        "data": data
    }), 200



def audd_recognition(frag_base64: str):
    """
    Sends a base64-encoded wav fragment to the Audd.io API for recognition.
    Returns a dictionary parsed from Audd.io's JSON response, or None if it fails.
    """
    # Decode the base64 string to raw wav bytes
    wav_bytes = base64.b64decode(frag_base64)

    # Prepare form fields
    data = {
        'api_token': KEY,
        'return': 'apple_music,spotify'
    }

    # Prepare the file parameter for request
    file = {
        'file': ('fragment.wav', wav_bytes, 'audio/wav')
    }

    # Make the POST request
    response = requests.post(AUDD_API, data=data, files=file)
    
    if response.status_code == 200:
        try:
            return response.json() 
        except Exception as e:
            print("Error parsing Audd.io response JSON:", e)
            return None
    else:
        print("Audd.io returned status code:", response.status_code)
        return None




if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)