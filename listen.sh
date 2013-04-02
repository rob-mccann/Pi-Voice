#!/bin/bash
arecord -D plughw:0,0 -f cd -t wav -d 6 -r 16000 | flac - -f --best --sample-rate 16000 -o out.flac; wget -O - -o /dev/null --post-file out.flac --header="Content-Type: audio/x-flac; rate=16000" http://www.google.com/speech-api/v1/recognize?lang=en | python main.py | festival --tts
