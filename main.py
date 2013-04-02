#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser
import wolframalpha
import codecs
import sys
import json
import pprint

jsonstr = sys.stdin.readlines()

jsonstr = jsonstr[0]

phrase = json.loads(jsonstr)


phrase = phrase['hypotheses'][0]['utterance']

config = ConfigParser.ConfigParser()

config.read('config.ini')

key = config.get('WolframAlpha', 'key')

client = wolframalpha.Client(key)

res = client.query(phrase)
sys.stderr.write(phrase + "\n")

try:
	if len(res.pods) == 0:
		raise StopIteration()

	for pod in res.results:
		if hasattr(pod.text, "encode"):
			print pod.text.replace(u"°",' degrees').encode('ascii', 'ignore')
			sys.exit(0)
		else:
			break

	print "I found a result but couldn't read it out to you. It could be a map, image or table."
except StopIteration:
	print "I couldn't find any results for the query, '" + phrase + "'"
