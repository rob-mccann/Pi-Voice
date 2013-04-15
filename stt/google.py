import tempfile
import audiotools
import requests
import json
import os

from ex.exception import NotUnderstoodException


class Google:
    def __init__(self, audio, rate=44100):
            self.audio = audio
            self.recordingRate = audio.rate() if audio.rate() else rate
            self.text = None

    def get_text(self):
        if not self.text is None:
            return self.text

        print "Converting to FLAC"
        (_, recording_flac_filename) = tempfile.mkstemp('.flac')
        recording_wav = audiotools.open(self.audio.filename())
        recording_wav.convert(recording_flac_filename,
                              audiotools.FlacAudio,)
                              #compression=audiotools.FlacAudio.COMPRESSION_MODES[8],
                              #progress=False)

        # turn the audio into useful text
        print "Sending to Google"
        google_speech_url = "http://www.google.com/speech-api/v1/recognize?lang=en"
        headers = {'Content-Type': 'audio/x-flac; rate= %d;' % self.recordingRate}
        recording_flac_data = open(recording_flac_filename, 'rb').read()
        r = requests.post(google_speech_url, data=recording_flac_data, headers=headers)

        # housekeeping
        os.remove(recording_flac_filename)
        self.audio.housekeeping()

        # grab the response
        response = r.text

        if not 'hypotheses' in response:
            raise NotUnderstoodException()

        # we are only interested in the most likely utterance
        phrase = json.loads(response)['hypotheses'][0]['utterance']
        print "Heard: " + phrase
        return str(phrase)
