#!/usr/bin/python
# -*- coding: utf-8 -*-

from inputs.microphone import Microphone
from actions.wolfram import Wolfram
from actions.db import DBPedia
from ex.exception import NotUnderstoodException

import sys
import os
import tts
import stt

class Job:
    def __init__(self, raw):
            self.raw_text = raw
            self.is_processed = False

    def get_is_processed(self):
        return self.is_processed

    def raw(self):
        return self.raw_text

    def naturalLanguage(self):
        # parse the raw text into semantic using nltk
        return self.raw


def main():
    if sys.platform == 'darwin':
        speaker = tts.OSX()
    else:
        # n.b. at the time of writing, this doesnt work on OSX
        speaker = tts.Google()

    try:
        audioInput = Microphone()

        audioInput.listen()

        speaker.say("Searching...")

        speech_to_text = stt.Google(audioInput)

        # speech_to_text = stt.Dummy('who was winston churchill?')

        job = Job(speech_to_text.get_text())

        plugins = {
            "db": DBPedia(speaker),
            "Wolfram": Wolfram(speaker, os.environ.get('WOLFRAM_API_KEY'))
        }

        for plugin in plugins:
            plugins[plugin].process(job)

        if not job.get_is_processed():
            speaker.say("Sorry, I couldn't find any results for the query, '" + job.raw() + "'.")

    except NotUnderstoodException:
        speaker.say("Sorry, I couldn't understand what you said.")


if __name__ == "__main__":
    main()


