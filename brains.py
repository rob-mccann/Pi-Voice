#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import wolframalpha
import os
import sys
import json

jsonstr = sys.stdin.readlines()

if len(jsonstr) == 0:
    print "I didn't quite understand what you said."
    sys.exit(0)

jsonstr = jsonstr[0]

phrase = json.loads(jsonstr)


phrase = phrase['hypotheses'][0]['utterance']

config = ConfigParser.ConfigParser()

key = os.environ.get('WOLFRAM_API_KEY')

if not key:
    print "I can't contact the knowledge base without an API key. Set one in an environment variable."
    sys.exit(0)

client = wolframalpha.Client(key)

res = client.query(phrase)
sys.stderr.write(phrase + "\n")

try:
    if len(res.pods) == 0:
        raise StopIteration()

    for pod in res.results:
        if hasattr(pod.text, "encode"):
            print pod.text.replace(u"°", ' degrees ').encode('ascii', 'ignore')
            sys.exit(0)
        else:
            break

    print "I found a result but could not read it out to you. It could be a map, image or table."
except StopIteration:
    print "I couldn't find any results for the query, '" + phrase + "'"
