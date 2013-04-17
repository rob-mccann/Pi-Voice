import os


class Festival:

    def say(self, text):
        print "Saying: " + text
        os.system('echo "%s" | festival --tts' % text)
