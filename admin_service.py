from flask import Flask, request, jsonify
from database import db
import base64

app = Flask(__name__)

@app.route('/upload_wav', methods=['POST'])
def upload_wav():
    """
    Upload a WAV file and store it in the SQLite database
    using the Repository class (db).
        
        Expects: 
        {
        "title": <"song name">,
        "artist": <"artist name">,
        "filename": <"file name">,
        "data": <base64-encoded WAV data>
        }
        
        Returns a JSON response indicating success or failure.
    """
    js = request.get_json()
    # Ensure the 'file' exists
    if js["filename"] == None or js["data"] == None:
        return jsonify({"error": "No 'filename' or 'data' key found in the request"}), 400
    
    file = js["filename"]
    if file == "" or type(file) != str:
        return jsonify({"error": "No selected file"}), 400

    wav_data = js["data"]
    if wav_data == "":
        return jsonify({"error": "Data is empty"}), 400
    
    title = js["title"]
    if title == "" or type(title) != str:
        return jsonify({"error": "Title not givern"}), 400

    artist = js["artist"]
    if artist == None:
        artist = "Unknown"

    try:
        base64.b64decode(wav_data)
    except Exception:
        return jsonify({"error": "Song data not valid"}), 400

    # Insert record into the database using the Repository
    new_id = db.insert({
        "title": title,
        "artist": artist,
        "filename": file,
        "data": wav_data
    })

    if new_id == None:
        return jsonify({"error": "Failed to add song to database"}), 500
    else:
        return jsonify({"message": "File uploaded successfully", "id": new_id}), 201


@app.route('/delete', methods=['DELETE'])
def delete_track():
    """Removes a given track from the database using the track's ID or title.
    Accepts a JSON body with either:
      {
        "id": <some integer>
      }
    or
      {
        "title": "<song title>"
      }

    Returns a JSON response indicating success or failure.
    """
    js = request.get_json()
    if js is None:
        return jsonify({"error": "No JSON payload"}), 400

    track_id = js.get("id")
    if track_id is None:
        # If 'id' is not provided, look for 'title'
        track_title = js.get("title")
        if track_title is not None:
            track_id = db.get_id(track_title)  # your method to get an ID from a title
        else:
            return jsonify({"error": "Missing 'id' or 'title' key in JSON"}), 400

    # Attempt removal from the repository
    rows_deleted = db.remove(track_id)
    if rows_deleted == 0:
        return jsonify({"error": f"No track found with id={track_id}"}), 404

    return jsonify({"message": f"Track with id={track_id} deleted successfully"}), 200


@app.route('/get_titles', methods=['GET'])
def get_titles():
    """Returns the titles of all songs in the database
    """
    titles = db.get_track_titles()
    return jsonify({"titles": titles}), 200



if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)