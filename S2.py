from flask import Flask, request, jsonify
from database import db
import base64

app = Flask(__name__)

@app.route('/delete', methods=['POST'])
def delete_track():
    js = request.get_json()

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)