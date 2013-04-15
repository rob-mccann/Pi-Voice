
import tempfile
import pyaudio
import sys
import wave
import os


class Microphone:

    def listen(self):
        print "Recording..."

        recording_rate = self.rate()

        # How many seconds should we record for?
        # Eventually we want to stop recording once the microphone returns to silence
        duration = 6

        # execute recording
        (_, recording_wav_filename) = tempfile.mkstemp('.wav')
        self.do_wav_recording(recording_wav_filename, recording_rate, duration=duration)

        self.recordedWavFilename = recording_wav_filename

        return self.recordedWavFilename

    def filename(self):
        return self.recordedWavFilename

    def rate(self):
        return 44100

    def housekeeping(self):
        os.remove(self.recordedWavFilename)

    def do_wav_recording(self, recording_filename, recording_rate, duration=5):
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
