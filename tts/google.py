import urllib
import tempfile
import audiotools
import requests
import os
import pyaudio
import wave


class Google:

    def say(self, text):
        print "Google Speaking: " + text

        urlencoded_words = urllib.quote_plus(text)
        (_, tts_mp3_filename) = tempfile.mkstemp('.mp3')
        request_url = "http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=%s" % urlencoded_words
        r = requests.get(request_url, headers={'User-agent': 'Mozilla'})
        f = open(tts_mp3_filename, 'wb')
        f.write(r.content)
        f.close()

        print "Got wav"

        print "converting to WAV"

        (_, tts_wav_filename) = tempfile.mkstemp('.wav')
        recording_wav = audiotools.open(tts_mp3_filename)
        recording_wav.convert(tts_wav_filename, audiotools.WaveAudio,)
        self.play_wav(tts_wav_filename)
        os.remove(tts_mp3_filename)

    def play_wav(self, filename):
        CHUNK = 1024
        wf = wave.open(filename, 'rb')

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()

        # open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(CHUNK)

        # play stream (3)
        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
