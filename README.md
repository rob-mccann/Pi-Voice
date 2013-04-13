Pi-Voice
========

The beginnings of a Star Trek-like computer. Run the program, speak into your microphone and hear the response from your speakers.

Ask it a question like "What was the temperature in London on the 13th July 1982?"

Requirements
------------
- alsa / alsa-utils
- python
- flac
- curl
- avconv
- Internet connection

Usage
-----
Make sure you've got all the requirements installed and run ```sh listen.sh```

Todo
----
1. Use Julius speech recogition as an always-on listener for the word "computer". Use that to trigger listen.sh.
2. Run the Julius recogniser as a service
3. Find a way of removing the need for out.flac and out.wav, or, at least, find a way of reducing collisions
4. Remove the linux dependency if feasible, at least, remove some of the requirements
5. Add Festival tts as an option
6. Create debian package so the program can be easily installed on the Raspberry Pi
