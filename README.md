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
- [Wolfram Alpha API key](http://products.wolframalpha.com/developers/)
- Internet connection

Usage
-----
1. Make sure you've got all the requirements installed
2. set the Wolfram Alpha API key as an environment variable ```export WOLFRAM_API_KEY='AAAAAA-AAAAAAAAAA'```
3. run ```python listen.py```

How it works
------------
When you run the command, it listens to the microphone for 6 seconds. It then sends the user's voice to Google who convert it to text. We then query Wolfram Alpha with what the user said. We send the response to Google TTS which then reads the response out to the user.

Todo
----
1. Use Julius speech recogition as an always-on listener for the word "computer". Use that to trigger listen.sh.
2. Run the Julius recogniser as a service
3. Find a way of removing the need for out.flac and out.wav, or, at least, find a way of reducing collisions
4. Remove the linux dependency if feasible, at least, remove some of the requirements
5. Add Festival tts as an option
6. Create debian package so the program can be easily installed on the Raspberry Pi
7. Remove the 6 second time limit. Find a way of listening for longer if there's still an input.

Contributors
------------

* [Rob McCann](http://robmccann.co.uk) - [@rob_mccann](http://twitter.com/rob_mccann)
