from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client.testdb

@app.route('/')
def home():
    return {"message": "Hello from Flask with MongoDB!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
