#!/usr/bin/python
# -*- coding: utf-8 -*-

import wolframalpha


class Wolfram:
    def __init__(self, tts, key):
            self.tts = tts
            self.key = key

    def process(self, job):
        if job.get_is_processed():
            return False
            
        print "Checking for API key..."

        if not self.key:
            self.tts.say("I can't contact the knowledge base without an API key. Set one in an environment variable.")
            return False

        self.say(self.query(job.raw(), self.key))
        job.is_processed = True

    def query(self, phrase, key):
        print "Querying Wolfram"
        client = wolframalpha.Client(key)
        res = client.query(phrase)

        print "Parsing response"
        try:
            if len(res.pods) == 0:
                # a bit messy but will do for now
                raise StopIteration()

            for pod in res.results:
                if hasattr(pod.text, "encode"):
                    # festival tts didn't recognise the utf8 degrees sign so we convert it to words
                    # there's probably more we need to add here
                    # convert to ascii too to prevent moans
                    return pod.text.replace(u"°", ' degrees ').encode('ascii', 'ignore')
                else:
                    break

            # TODO offer to display the result instead of a display is detected
            return "I found a result but could not read it out to you. It could be a map, image or table."

        except StopIteration:
            return "Sorry, I couldn't find any results for the query, '" + phrase + "'"

    def say(self, text):
        return self.tts.say(text)
