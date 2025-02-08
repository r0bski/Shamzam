from database import db
from flask import Flask, request

app  = Flask(__name__)






if __name__ == "__main__":
    app.run(host="localhost",port=3000)