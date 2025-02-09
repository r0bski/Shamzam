# app.py
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
    if file== "":
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

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)