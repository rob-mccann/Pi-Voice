
from array import array
from struct import pack

import tempfile
import pyaudio
import sys
import wave
import os


class Microphone:

    def listen(self):
        print "Recording..."

        recording_rate = self.rate()

        # execute recording
        (_, recording_wav_filename) = tempfile.mkstemp('.wav')
        self.do_wav_recording(recording_wav_filename, recording_rate)

        self.recordedWavFilename = recording_wav_filename

        return self.recordedWavFilename

    def filename(self):
        return self.recordedWavFilename

    def rate(self):
        return 44100

    def housekeeping(self):
        os.remove(self.recordedWavFilename)

    def is_silent(self, sound_data, threshold):
        return max(sound_data) < threshold

    def add_silence(self, sound_data, seconds, recording_rate):
        r = array('h', [0 for i in xrange(int(seconds*recording_rate))])
        r.extend(sound_data)
        r.extend([0 for i in xrange(int(seconds*recording_rate))])
        return r

    def do_wav_recording(self, recording_filename, recording_rate):
        THRESHOLD = 2000            # Set threshold of volume to consider as silence
        NUM_SILENT = 40             # Set amt of silence to accept before ending recording
        CHUNK = 1024    
        FORMAT = pyaudio.paInt16
        CHANNELS = 2

        if sys.platform == 'darwin':
            CHANNELS = 1

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=recording_rate,
                        input=True,
                        frames_per_buffer=CHUNK)

        num_silent = 0              
        speech_started = False       
        r = array('h')

        print("* recording")

        while 1:
            sound_data = array('h', stream.read(CHUNK))
            if sys.byteorder == 'big':
                sound_data.byteswap()
            r.extend(sound_data)

            silent = self.is_silent(sound_data, THRESHOLD)

            if silent and speech_started:
                num_silent += 1
            elif not silent and not speech_started:
                speech_started = True

            if speech_started and num_silent > NUM_SILENT:
                break

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        data = self.add_silence(r, 0.5, recording_rate)
        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open(recording_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(recording_rate)
        wf.writeframes(b''.join(data))
        wf.close()
