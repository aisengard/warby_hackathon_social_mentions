import binascii
from hashlib import sha1
import hmac
import random
import string
import time
from urllib import quote_plus


#returns oAuth authorization header value
def generate_oauth(method, url, params, consumer_key, consumer_secret,
                   access_token, access_token_secret):

    oauth_nonce = "".join([random.choice(string.ascii_letters + string.digits) for _ in xrange(30)])

    auth_dict = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': oauth_nonce,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_token': access_token,
        'oauth_timestamp': str(int(time.time())),
        'oauth_version': '1.0'}

    oauth_dict = dict(params.items()+auth_dict.items())
    encoded_param_string = generate_param_string(oauth_dict)

    sig_base_string = method+"&"+quote_plus(url)+"&"+quote_plus(encoded_param_string)
    signing_key = quote_plus(consumer_secret)+"&"+quote_plus(access_token_secret)

    hashed = hmac.new(signing_key, sig_base_string, sha1)
    oauth_signature = binascii.b2a_base64(hashed.digest())[:-1]
    auth_dict['oauth_signature'] = oauth_signature

    return generate_oauth_string(auth_dict)


def generate_param_string(auth_dict):
    param_string = ""
    sorted_key_list = sorted(auth_dict)
    first = True
    for key in sorted_key_list:
        val = auth_dict[key]
        temp_string = ""
        if first:
            first = False
        else:
            temp_string = "&"
        temp_string = temp_string + quote_plus(key)+'='+quote_plus(val)
        param_string += temp_string

    return param_string


def generate_oauth_string(auth_dict):
    auth_string = "OAuth "
    sorted_key_list = sorted(auth_dict)
    first = True
    for key in sorted_key_list:
        val = auth_dict[key]
        temp_string = ""
        if first:
            first = False
        else:
            temp_string = ", "
        temp_string = temp_string + quote_plus(key)+'='+'"'+quote_plus(val)+'"'
        auth_string += temp_string

    return auth_string