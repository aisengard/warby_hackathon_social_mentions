import api.tumblr
import api.twitter


def routes():
    return [
        (r'/tumblr', api.tumblr.TumblrStreamHandler),
        (r'/twitter', api.twitter.TwitterStreamHandler)]