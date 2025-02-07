from flask import Flask, render_template, request, g, send_from_directory
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import os

app = Flask(__name__)

def get_mongo_client():
    if 'mongo_client' not in g:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI environment variable must be set")
        g.mongo_client = MongoClient(uri)
    return g.mongo_client

@app.route('/')
def display_news():
    pass

if __name__ == "__main__":
    app.run(debug=True)