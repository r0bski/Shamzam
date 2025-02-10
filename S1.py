from flask import Flask, request, jsonify
from database import db
import base64

app = Flask(__name__)

@app.route('/upload_wav', methods=['POST'])
def upload_wav():
    """
    Upload a WAV file and store it in the SQLite database
    using the Repository class (db).
    """
    js = request.get_json()
    # Ensure the 'file' part exists
    if js["filename"]== None or js["data"] == None:
        return jsonify({"error": "No 'filename' or 'data' key found in the request"}), 400
    
    file = js["filename"]
    if file == "":
        return jsonify({"error": "No selected file"}), 400

    wav_data = js["data"]
    if wav_data == "":
        return jsonify({"error": "Data is empty"}), 400

    title = js["title"]
    artist = js["artist"]
    if title == None:
        title = "Unknown"
    if artist == None:
        artist = "Unknown"

    # Insert record into the database using the Repository
    new_id = db.insert({
        "title": title,
        "artist": artist,
        "filename": file,
        "data": wav_data
    })

    return jsonify({"message": "File uploaded successfully", "id": new_id}), 201


@app.route('/delete', methods=['POST'])
def delete_track():
    js = request.get_json()
    if js is None:
        return jsonify({"error": "No JSON payload"}), 400

    track_id = js.get("id")
    if track_id is None:
        if js.get("title") != None:
            track_id = db.get_id(js["title"])
        else:
            return jsonify({"error": "Missing 'id' key in JSON"}), 400

    # Call remove method on the Repository
    rows_deleted = db.remove(track_id)
    if rows_deleted == 0:
        return jsonify({"error": f"No track found with id={track_id}"}), 404

    return jsonify({"message": f"Track with id={track_id} deleted successfully"}), 200



if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)