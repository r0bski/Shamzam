from flask import Flask, request, jsonify
from database import db
import base64

app = Flask(__name__)

@app.route('/get_song', methods=['POST'])
def get_song():
    js = request.get_json()
    title = js.get("title")
    if title is None:
        return jsonify({"error": "No 'title' found in the request"}), 400
    id = db.get_id(title)
    row = db.lookup(id)
    if row is None:
        return jsonify({"error": "Song not found in database"}), 400
    data = row["data"]
    return jsonify({"message":"Successfully retreved song", "data":data}), 200

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)