import json
import requests
import time
import tornado.httpclient
import tornado.websocket

from config import TWITTER as cfg
from . import oauth

stream_filter_url = "https://stream.twitter.com/1.1/statuses/filter.json"


class TwitterStreamHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, _):
        return True

    def on_message(self, message):
        msg = json.loads(message)
        if msg.get('change_keyword'):
            if hasattr(self, 'session'):
                self.session.close()
            self.status_generator = self.filter_stream_generator(msg.get('keyword_filter'))
        if hasattr(self, 'status_generator'):
            self.write_message(self.status_generator.next())
        else:
            self.status_generator = self.filter_stream_generator(msg.get('keyword_filter'))
            self.write_message(self.status_generator.next())

    def filter_stream_generator(self, track):
        post_reqs = {'track': track}
        oauth_token = oauth.generate_oauth(
            'POST', stream_filter_url, post_reqs,
            cfg.get('consumer_key'), cfg.get('consumer_secret'),
            cfg.get('access_token'), cfg.get('access_token_secret'))

        self.session = requests.Session()
        headers = {"Authorization": oauth_token}
        req = requests.Request("POST", stream_filter_url, headers=headers, data=post_reqs).prepare()

        resp = self.session.send(req, stream=True)

        for status in resp.iter_lines():
            if status:
                yield status

