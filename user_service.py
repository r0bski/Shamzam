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
        base64: Encoded song data
    """
    # Retrive song title from request
    title = request.args.get("title")
    if title is None:
        return jsonify({"error": "No 'title' found in the request"}), 400
    
    # Get id of song in database
    id = db.get_id(title)
    # Look up the song in the database using its id
    row = db.lookup(id)

    if row is None or id is None:
        return jsonify({"error": "Song not found in database"}), 404
    data = row["data"]

    # Return the song data if it was successful
    return jsonify({"message":"Successfully retreved song", "data":data}), 200


@app.route('/frag_recognition', methods=['POST'])
def frag_recognition():
    """
    1) Decodes the base64 fragment and sends to Audd.io for recognition.
    2) If recognized, get the song title from Audd.io's response.
    3) Look up the title in the local database.
    4) If found, return the stored data for that track.

    Expects:
    {
      "fragment": "<base64 encoded WAV data>"
    }
    """
    js = request.get_json()
    if js is None:
        return jsonify({"error": "No JSON payload"}), 400

    # Get base64 encoded song fragment
    frag_base64 = js.get("fragment")
    if not frag_base64:
        return jsonify({"error": "Song fragment data not in JSON payload"}), 400

    # Recognise using Audd.io
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

    # Get song from database
    song_dict = db.lookup(track_id)
    if not song_dict:
        return jsonify({"error": "Song not found in database"}), 404

    artist = song_dict.get("artist", "Unknown Artist")
    data = song_dict.get("data", "")

    # Return base64 encoded song data
    return jsonify({
        "message": f"Successfully retrieved '{title}' by {artist}",
        "data": data
    }), 200



def audd_recognition(frag_base64: str):
    """Sends a base64-encoded wav fragment to the Audd.io API for recognition.
        Returns a dictionary parsed from Audd.io's json response, or None if it fails.

    Args:
        frag_base64 (str): base64 encoded song fragment

    Returns:
        dict: dictionary containing json response from Audd.io
        None: if it fails to recognise the song
    """
    # Decode the base64 string to wav bytes
    wav_bytes = base64.b64decode(frag_base64)

    # define json data
    data = {
        'api_token': KEY,
        'return': 'apple_music,spotify'
    }

    # Prepare the file for request
    file = {
        'file': ('fragment.wav', wav_bytes, 'audio/wav')
    }

    # Make the post request
    response = requests.post(AUDD_API, data=data, files=file)
    
    # Check response code
    if response.status_code == 200:
        # Try return the API's response
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