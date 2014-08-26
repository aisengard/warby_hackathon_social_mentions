import requests
import tornado.httpclient
import tornado.websocket

from config import TUMBLR as cfg

stream_filter_url = "http://api.tumblr.com/v2/tagged"


class TumblrStreamHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, _):
        return True

    def on_message(self, message):
        for status in self.filter_stream_generator(message):
            self.write_message(status)

    def filter_stream_generator(self, tag):
        resp = requests.get(stream_filter_url,
                            params={'tag': tag, 'api_key': cfg.get('consumer_key')})

        response = resp.json().get('response')
        for result in response:
            if result:
                yield result

