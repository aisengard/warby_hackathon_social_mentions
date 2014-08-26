import base64
import random
import string
import time
from hashlib import sha1
import hmac
import binascii
import json

import urllib, urllib2
from urllib import quote_plus

# returns access_token
def authRequest(consumerKey, consumerSecret, token_url):

    bearerToken = consumerKey+":"+consumerSecret
    b64BearerToken = base64.b64encode(bearerToken)

    data = {}
    headers = {}
    headers['Authorization'] = 'Basic '+b64BearerToken
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF8'

    data['grant_type'] = 'client_credentials'
    data = urllib.urlencode(data)

    req = urllib2.Request(token_url, data, headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print e
        return

    jsonResp = json.loads(response.read())
    return jsonResp.get('access_token')

#returns oAuth authorization header value
def generateOAuth(method, url, params, consumerKey, consumerSecret, accessToken, accessTokenSecret):

    oAuthNonce = "".join([random.choice(string.ascii_letters + string.digits) for _ in xrange(30)])

    authDict = {}
    authDict['oauth_consumer_key'] = consumerKey
    authDict['oauth_nonce'] = oAuthNonce
    authDict['oauth_signature_method'] = "HMAC-SHA1"
    authDict['oauth_token'] = accessToken
    authDict['oauth_timestamp'] = str(int(time.time()))
    authDict['oauth_version'] = "1.0"

    oAuthDict = dict(params.items()+authDict.items())
    encodedParamString = generateParamString(oAuthDict)

    sigBaseString = method+"&"+quote_plus(url)+"&"+quote_plus(encodedParamString)
    signingKey = quote_plus(consumerSecret)+"&"+quote_plus(accessTokenSecret)

    hashed = hmac.new(signingKey, sigBaseString, sha1)

    oAuthSignature = binascii.b2a_base64(hashed.digest())[:-1]

    authDict['oauth_signature'] = oAuthSignature

    return generateOAuthString(authDict)

def generateParamString(authDict):
    paramString = ""
    sortedKeyList = sorted(authDict)
    first = True
    for key in sortedKeyList:
        val = authDict[key]
        tempString = ""
        if first: first=False
        else: tempString = "&"
        tempString = tempString + quote_plus(key)+'='+quote_plus(val)
        paramString = paramString + tempString

    return paramString

def generateOAuthString(authDict):
    authString = "OAuth "
    sortedKeyList = sorted(authDict)
    first = True
    for key in sortedKeyList:
        val = authDict[key]
        tempString = ""
        if first: first=False
        else: tempString = ", "
        tempString = tempString + quote_plus(key)+'='+'"'+quote_plus(val)+'"'
        authString = authString + tempString

    return authString