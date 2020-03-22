import time

from flask import Flask, jsonify

from model.tutu import is_cat
from mongo import DBClient
from proto.client import Client
from utils import get_usernames
import threading


usernames = get_usernames()
client = Client()
mongo = DBClient()

app = Flask(__name__)


def parse_insta():
    while True:
        profiles = client.get_data(usernames).profiles
        for profile in profiles:
            for post in profile.posts:
                if post.type == 0:
                    if not mongo.insta_id_exists(post.inst_id):
                        data = {
                            'insta_id': post.inst_id,
                            'username': profile.username,
                            'url': post.link,
                            'is_cat': is_cat(post.link)
                        }
                        mongo.insert_doc(data)
        time.sleep(1200)


@app.route('/cats/')
def get_cats():
    posts_with_cats = mongo.get_all_cats()
    return jsonify(posts_with_cats)


if __name__ == '__main__':
    download_thread = threading.Thread(target=parse_insta)
    download_thread.start()
    app.run(port=8080)
