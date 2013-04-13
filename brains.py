#!/usr/bin/python
# -*- coding: utf-8 -*-
import wolframalpha
import os
import sys
import json

# Read the input from Google's speech recognition
jsonstr = sys.stdin.readlines()

if len(jsonstr) == 0:
    print "I didn't quite understand what you said."
    sys.exit(0)

# There's only ever one line (I hope)
jsonstr = jsonstr[0]

# parse the json
phrase = json.loads(jsonstr)

# grab what the user said
phrase = phrase['hypotheses'][0]['utterance']

# output to stderr for debug purposes
sys.stderr.write(phrase + "\n")

# grab the user's api key
key = os.environ.get('WOLFRAM_API_KEY')

if not key:
    print "I can't contact the knowledge base without an API key. Set one in an environment variable."
    sys.exit(0)

client = wolframalpha.Client(key)

# ask wolfram alpha for any info based on the query
res = client.query(phrase)

try:
    if len(res.pods) == 0:
        # a bit messy but will do for now
        raise StopIteration()

    for pod in res.results:
        if hasattr(pod.text, "encode"):
            # festival tts didn't recognise the utf8 degrees sign so we convert it to words
            # there's probably more we need to add here
            # convert to ascii too to prevent moans
            print pod.text.replace(u"°", ' degrees ').encode('ascii', 'ignore')
            sys.exit(0)
        else:
            break

    # TODO offer to display the result instead of a display is detected
    print "I found a result but could not read it out to you. It could be a map, image or table."
except StopIteration:
    print "I couldn't find any results for the query, '" + phrase + "'"
