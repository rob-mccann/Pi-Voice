#!/usr/bin/python
# -*- coding: utf-8 -*-

from stt.google import Google as GoogleSTT
from stt.dummy import Dummy as DummySTT
from inputs.microphone import Microphone
from actions.wolfram import Wolfram
from actions.db import DBPedia
from ex.exception import NotUnderstoodException
from tts.google import Google as GoogleTTS
from tts.osx import OSX as OSXTTS

import sys
import os


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
        speaker = OSXTTS()
    else:
        # n.b. at the time of writing, this doesnt work on OSX
        speaker = GoogleTTS()

    try:
        audioInput = Microphone()

        audioInput.listen()

        speaker.say("Searching...")

        speech_to_text = GoogleSTT(audioInput)

        # speech_to_text = DummySTT('who was winston churchill?')

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


