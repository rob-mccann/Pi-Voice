#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import sys
import tempfile
import requests
import audiotools
import os
import json
import wolframalpha
import urllib

wolframalpha_key = os.environ.get('WOLFRAM_API_KEY')

if not wolframalpha_key:
    print "I can't contact the knowledge base without an API key. Set one in an environment variable."
    sys.exit(0)

def main():
    print "recording"
    recording_rate = 44100
    duration = 6
    (_, recording_wav_filename) = tempfile.mkstemp('.wav')
    do_wav_recording(recording_wav_filename, recording_rate, duration=duration)

    print "converting to FLAC"
    (_, recording_flac_filename) = tempfile.mkstemp('.flac')
    recording_wav = audiotools.open(recording_wav_filename)
    recording_wav.convert(recording_flac_filename,
                          audiotools.FlacAudio,)
                          #compression=audiotools.FlacAudio.COMPRESSION_MODES[8],
                          #progress=False)

    print "sending to Google"
    google_speech_url = "http://www.google.com/speech-api/v1/recognize?lang=en"
    headers = {'Content-Type': 'audio/x-flac; rate= %d;' % recording_rate}
    recording_flac_data = open(recording_flac_filename, 'rb').read()
    r = requests.post(google_speech_url, data=recording_flac_data, headers=headers)
    response = r.text
    os.remove(recording_wav_filename)
    os.remove(recording_flac_filename)

    if 'hypotheses' in response:
        phrase = json.loads(response)['hypotheses'][0]['utterance']

        print "Looking question up in Wolfram Alpha"
        answer = query_wolfram_alpha(str(phrase))
        if answer is not None:
            say(answer)
        else:
            say('Sorry, there was not reply from Wolfram Alpha.')
    else:
        print "Google couldn't interpret what was said."

def query_wolfram_alpha(phrase):
    client = wolframalpha.Client(wolframalpha_key)

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
                return pod.text.replace(u"°", ' degrees ').encode('ascii', 'ignore')
            else:
                break

        # TODO offer to display the result instead of a display is detected
        return "I found a result but could not read it out to you. It could be a map, image or table."
    except StopIteration:
        return "Sorry, I couldn't find any results for the query, '" + phrase + "'"

def do_wav_recording(recording_filename, recording_rate, duration = 5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    if sys.platform == 'darwin':
        CHANNELS = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=recording_rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(recording_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def say(sentence):
    if sys.platform == 'darwin':
        os.system('say "%s"' % sentence)
    else:
        urlencoded_words = urllib.quote_plus(sentence)
        (_, tts_mp3_filename) = tempfile.mkstemp('.mp3')
        request_url = "http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=%s" % urlencoded_words
        r = requests.get(request_url, headers={'User-agent': 'Mozilla'})
        f = open(tts_mp3_filename,'wb')
        f.write(r.content)
        f.close()

        os.system('aplay %s' % tts_mp3_filename)
        os.remove(tts_mp3_filename)
        # the process doesn't work at the moment, audiotools doesn't recognise
        # the filetype, even though the file returned by google is definitely
        # a mp3-file.
        #print "converting to WAV"
        #print tts_mp3_filename
        #(_, tts_wav_filename) = tempfile.mkstemp('.wav')
        #recording_wav = audiotools.open(tts_mp3_filename)
        #recording_wav.convert(tts_wav_filename, audiotools.WaveAudio,)
        #play_wav(tts_wav_filename)

def play_wav(filename):
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

if __name__ == "__main__":
    main()
