import requests
import tornado.gen
import tornado.httpclient
import tornado.websocket

from . import oauth

stream_filter_url = "https://stream.twitter.com/1.1/statuses/filter.json"


class TwitterStreamHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, _):
        return True

    def on_message(self, message):
        for status in self.filter_stream_generator(message):
            self.write_message(status)

    def filter_stream_generator(self, track):
        post_reqs = {'track': track}
        oauth_token = oauth.generateOAuth(
            'POST', stream_filter_url, post_reqs,
            'A09ADIWm5ObRfrzwlJTQ', 'JlFOVERuOvmX6tHOl9SKyVjwAiCKz0Kn7hXN4bnSnrk',
            '226017037-BQx93ektXGfrQJ3ZXrvsJdsQTlKMcFlOHVeDtWGQ', 'ouTj9F4ryjsjeTeNC2Euew1UGiLERpKsaeo51eAonbeJu')

        s = requests.Session()
        headers = {"Authorization": oauth_token}
        req = requests.Request("POST", stream_filter_url, headers=headers, data=post_reqs).prepare()

        resp = s.send(req, stream=True)

        for status in resp.iter_lines():
            if status:
                yield status

