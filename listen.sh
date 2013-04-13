#!/bin/bash

# Records the microphone input and converts it into something that google can understand
arecord -D plughw:0,0 -f cd -t wav -d 6 -r 16000 | flac - -f --best --sample-rate 16000 -o out.flac

# Sends the microphone recording to Google who respond with the text. Our python script parses it and decides what to say
WORDS=$(wget -O - -o /dev/null --post-file out.flac --header="Content-Type: audio/x-flac; rate=16000" http://www.google.com/speech-api/v1/recognize?lang=en | python brains.py)
# housekeeping
rm out.flac

# We've now decided what to say, output it to stderr for now
echo "Saying: $WORDS" 1>&2

# Url encode it for Google's TTS
URLENCODED_WORDS=$(python -c "import sys, urllib as ul; sys.argv.pop(0); print ul.quote_plus(' '.join(sys.argv))" $WORDS)
echo "$URLENCODED_WORDS" 1>&2

# tried piping straight to aplay but just got silence and no errors :/
curl -sA "Mozilla" "http://translate.google.com/translate_tts?ie=utf-8&tl=en&q=$URLENCODED_WORDS" | avconv -loglevel panic -i - -f wav out.wav
aplay out.wav

# housekeeping
rm out.wav
