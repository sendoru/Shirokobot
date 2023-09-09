import pymongo
import flask
import json
import src
from threading import Thread

with open("config.json") as f:
    json_obj = json.load(f)

    MONGODB_HOST = json_obj[0]["MONGODB_HOST"]
    MONGODB_PORT = json_obj[0]["MONGODB_PORT"]
    MONGODB_USERNAME = json_obj[0]["MONGODB_USERNAME"]
    MONGODB_PASSWORD = json_obj[0]["MONGODB_PASSWORD"]
    HASH = json_obj[0]["HASH"]

mongo_client = pymongo.MongoClient(
    host=MONGODB_HOST,
    port=MONGODB_PORT,
    )

if not 'students' in mongo_client.local.list_collection_names():
    with open("data/students.json", encoding='utf-8') as f:
        json_obj = json.load(f)
        mongo_client.local.get_collection('students').insert_many(json_obj)

app = flask.Flask(__name__)
app.register_blueprint(src.api.gacha.bp)
app.config['MONGO_CLIENT'] = mongo_client
with app.app_context():
    app.mongo_client = mongo_client

mongo_client

@app.route('/')
def hello_world():
    return 'Hello, World!'

def run():
    app.run(host='localhost', port=5555)

def web():
    thread = Thread(target=run)
    thread.start()

if __name__ == "__main__":
    app.run(host='localhost', port=5555)