Pi-Voice
========

The beginnings of a Star Trek-like computer. Run the program, speak into your microphone and hear the response from your speakers.

Ask it a question like "What was the temperature in London on the 13th July 1982?"

Requirements
------------

- python: audiotools
- python: pyaudio
- python: requests
- python: quepy
- python: numpy
- [Wolfram Alpha API key](http://products.wolframalpha.com/developers/) - note, their free, non-commercial licence is limited to 2,000 queries/month.
- Internet connection

Usage
-----
1. Make sure you've got all the requirements installed
2. set the Wolfram Alpha API key as an environment variable ```export WOLFRAM_API_KEY='AAAAAA-AAAAAAAAAA'```
3. run ```python listen.py```

How it works
------------
When you run the command, it listens to the microphone. Once it detects noise has returned to silence, it then sends the user's voice to Google who convert it to text. We then query Wolfram Alpha with what the user said. We send the response to Google TTS which then reads the response out to the user.

Todo
----
1. Use Julius speech recogition as an always-on listener for the word "computer". Use that to trigger listen.sh.
2. Run the Julius recogniser as a service
3. Allow plugins to self-regulate their results by weighting them. listen.py chooses the highest weighted.
4. Allow plugins to run asynchronously.
5. Allow user to specify tts/stt engine as a command line option
6. Create debian package so the program can be easily installed on the Raspberry Pi


Contributors
------------

* [Rob McCann](http://robmccann.co.uk) - [@rob_mccann](http://twitter.com/rob_mccann)
* Thomas Weng
